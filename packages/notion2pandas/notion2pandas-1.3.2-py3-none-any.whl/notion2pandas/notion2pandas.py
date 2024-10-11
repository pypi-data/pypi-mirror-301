import time
import json
import math

import pandas as pd

from notion_client import Client, APIErrorCode, APIResponseError
from notion_client.errors import HTTPResponseError, RequestTimeoutError
from notion_client.helpers import collect_paginated_api

from . import n2p_read_write


class NotionMaxAttemptsException(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class Notion2PandasClient(Client):
    """Extension of Client from notion_client.

    Attributes:
        secondsToRetry: .
        callsLimitThreshold: .
        maxAttemptsExecutioner: .
    """

    _ROW_HASH_KEY = 'Row_Hash'
    _ROW_PAGEID_KEY = 'PageID'

    # It's not in the official documentation, but it seems there is a limit of 2700 API calls in 15 minutes.
    # https://notionmastery.com/pushing-notion-to-the-limits/#rate-limits
    # WIP
    _RATE_LIMIT_THRESHOLD = 900  #60 * 15
    _CALLS_LIMIT_THRESHOLD = 2700

    def __init__(self, **kwargs):
        self.__set_n2p_arg(kwargs, 'secondsToRetry', 30)
        self.__set_n2p_arg(kwargs, 'maxAttemptsExecutioner', 3)

        super().__init__(**kwargs)

        self.read_only_columns = {"last_edited_time", "last_edited_time",
                                  "files", "created_time", "rollup", "unique_id", "last_edited_by",
                                  "button", "formula", "created_by"}

        self.read_write_lambdas = {
            'title': (n2p_read_write.title_read, n2p_read_write.title_write),
            'rich_text': (n2p_read_write.rich_text_read, n2p_read_write.rich_text_write),
            'checkbox': (n2p_read_write.checkbox_read, n2p_read_write.checkbox_write),
            'created_time': (n2p_read_write.created_time_read, n2p_read_write.created_time_write),
            'number': (n2p_read_write.number_read, n2p_read_write.number_write),
            'email': (n2p_read_write.email_read, n2p_read_write.email_write),
            'url': (n2p_read_write.url_read, n2p_read_write.url_write),
            'multi_select': (n2p_read_write.multi_select_read, n2p_read_write.multi_select_write),
            'select': (n2p_read_write.select_read, n2p_read_write.select_write),
            'date': (n2p_read_write.date_read, n2p_read_write.date_write),
            'date_range': (n2p_read_write.range_date_read, n2p_read_write.range_date_write),
            'files': (n2p_read_write.files_read, n2p_read_write.files_write),
            'formula': (n2p_read_write.formula_read, n2p_read_write.formula_write),
            'phone_number': (n2p_read_write.phone_number_read, n2p_read_write.phone_number_write),
            'status': (n2p_read_write.status_read, n2p_read_write.status_write),
            'unique_id': (n2p_read_write.unique_id_read, n2p_read_write.unique_id_write),
            'created_by': (n2p_read_write.created_by_read, n2p_read_write.created_by_write),
            'last_edited_time': (n2p_read_write.last_edited_time_read, n2p_read_write.last_edited_time_write),
            'string': (n2p_read_write.string_read, n2p_read_write.string_write),
            'last_edited_by': (n2p_read_write.last_edited_by_read, n2p_read_write.last_edited_by_write),
            'button': (n2p_read_write.button_read, n2p_read_write.button_write),
            'relation': (n2p_read_write.relation_read, n2p_read_write.relation_write),
            'rollup': (n2p_read_write.rollup_read, n2p_read_write.rollup_write),
            'people': (n2p_read_write.people_read, n2p_read_write.people_write)
        }

        self.update_switcher()

    def update_switcher(self):
        """Update the switcher dynamically based on read_write_lambdas"""
        self.switcher = {key: lambdas for key, lambdas in self.read_write_lambdas.items()}

    def set_lambdas(self, key, new_read, new_write):
        """Generic method to update the read/write lambdas for a given key"""
        if key in self.read_write_lambdas:
            self.read_write_lambdas[key] = (new_read, new_write)
            self.update_switcher()  # Update the switcher after modification
        else:
            raise KeyError(f"'{key}' does not exist in read_write_lambdas")

    """Since Notion has introduced limits on requests to their APIs (https://developers.notion.com/reference/request-limits), 
       this method can repeat the request to the Notion APIs at predefined time intervals
       until a result is obtained or if the maximum limit of attempts is reached."""

    def _notionExecutor(self, api_to_call, **kwargs):
        attempts = self.maxAttemptsExecutioner
        current_calls = 0
        while attempts > 0:
            try:
                result = api_to_call(**kwargs)
                current_calls += 1
                return result
            except HTTPResponseError as error:
                print('Caught exception: ' + str(error))
                attempts -= 1
                if isinstance(error, APIResponseError):
                    print('Error code: ' + error.code)
                    if error.code != APIErrorCode.InternalServerError and error.code != APIErrorCode.ServiceUnavailable:
                        print(error)
                        print(APIResponseError)
                        # raise APIErrorCode.ObjectNotFound
                else:
                    # Other error handling code
                    print(error)
                # Wait secondsToRetry before retry
                time.sleep(self.secondsToRetry)
            except RequestTimeoutError as error:
                print('Caught exception: ' + str(error))
                attempts -= 1
            if attempts == 0:
                raise NotionMaxAttemptsException(
                    "NotionMaxAttemptsException") from None
            print('[_notionExecutor] Remaining attempts: ' + str(attempts))
        return None

    def get_database_columns(self, database_ID):
        return self._notionExecutor(
            self.databases.retrieve, **{'database_id': database_ID})

    def create_page(self, parent_id, properties=None):
        created_page = self._notionExecutor(self.pages.create, **{'parent': {"database_id": parent_id},
                                                                  'properties': properties})
        return created_page.get('id')

    def _update_page(self, page_ID, properties):
        updated_page = self._notionExecutor(self.pages.update, **{'page_id': page_ID,
                                                                  'properties': properties})
        return updated_page.get('id')

    def update_page(self, page_ID, **kwargs):
        kwargs['page_id'] = page_ID
        updated_page = self._notionExecutor(self.pages.update, **kwargs)
        return updated_page.get('id')

    def retrieve_page(self, page_ID):
        return self._notionExecutor(
            self.pages.retrieve, **{'page_id': page_ID})

    def delete_page(self, page_ID):
        self._notionExecutor(
            self.blocks.delete, **{'block_id': page_ID})

    def delete_rows_and_pages(self, df, rows_to_delete_indexes: list):
        PageID = df['PageID']
        for row_index in rows_to_delete_indexes:
            PageID = df.loc[row_index, 'PageID']
            self.delete_page(PageID)
        df.drop(rows_to_delete_indexes, inplace=True)

    def retrieve_block(self, block_ID):
        return self._notionExecutor(
            self.blocks.retrieve, **{'block_id': block_ID})

    def retrieve_block_children_list(self, page_ID):
        return self._notionExecutor(
            self.blocks.children.list, **{'block_id': page_ID})

    def update_block(self, block_ID, field, field_value_updated):
        return self._notionExecutor(
            self.blocks.update, **{'block_id': block_ID, field: field_value_updated})

    def __row_hash(self, row):
        row_dict = row.to_dict()
        if self._ROW_HASH_KEY in row_dict:
            del row_dict[self._ROW_HASH_KEY]
        return self.__calculate_dict_hash(row_dict)

    def __calculate_dict_hash(self, d):
        serialized_dict = json.dumps(d, sort_keys=True)
        return hash(serialized_dict)

    def __get_database_columnsAndTypes(self, database_ID):
        columns = self.get_database_columns(database_ID)
        if columns is None:
            return None
        return list(map(lambda notion_property:
                        (columns.get('properties').get(notion_property).get('name'),
                         columns.get('properties').get(notion_property).get('type')),
                        columns.get('properties')))

    def from_notion_DB_to_dataframe(self, database_ID: str, filter_params=None):
        return self.from_notion_DB_to_dataframe_kwargs(database_ID, filter_params = filter_params)

    def from_notion_DB_to_dataframe_kwargs(self, database_ID: str, **kwargs):
        if 'filter_params' not in kwargs or kwargs['filter_params'] is None:
            filter_params = {}
        else:
            filter_params = kwargs['filter_params']
        if 'columns_from_page' in kwargs:
            columns_from_page = list(kwargs['columns_from_page'].items())
        else:
            columns_from_page = []
        if 'columns_from_blocks' in kwargs:
            columns_from_blocks = list(kwargs['columns_from_blocks'].items())
        else:
            columns_from_blocks = []
        results = self._notionExecutor(
            collect_paginated_api,
            **{'function': self.databases.query, **filter_params, "database_id": database_ID})
        database_data = []
        for result in results:
            prop_dict = {}
            for notion_property in result.get("properties"):
                prop_dict[str(notion_property)] = n2p_read_write.read_value_from_notion(
                    result.get("properties").get(notion_property), self.switcher)
            page_id = result.get("id")
            prop_dict[self._ROW_PAGEID_KEY] = page_id
            self._add_custom_columns(page_id, self.retrieve_page, prop_dict, columns_from_page)
            self._add_custom_columns(page_id, self.retrieve_block_children_list, prop_dict, columns_from_blocks)
            database_data.append(prop_dict)
        df = pd.DataFrame(database_data)
        df[self._ROW_HASH_KEY] = df.apply(
            lambda row: self.__row_hash(row), axis=1)
        return df

    def _add_custom_columns(self, page_id, get_data_function, prop_dict, columns_dict):
        if len(columns_dict) > 0:
            notion_data = get_data_function(page_id)
            for column_name, function in columns_dict:
                prop_dict[column_name] = function(notion_data)
    def update_notion_DB_from_dataframe(self, database_ID, df):
        columns = self.__get_database_columnsAndTypes(database_ID)
        for index, row in df.iterrows():
            current_row_hash = self.__row_hash(row)
            if current_row_hash != row[self._ROW_HASH_KEY]:
                prop_dict = {}
                for column in columns:
                    column_name = column[0]
                    column_type = column[1]
                    if column_type in self.read_only_columns:
                        continue
                    prop_dict[column_name] = n2p_read_write.write_value_to_notion(
                        row[column_name], column_type, self.switcher)
                if row[self._ROW_PAGEID_KEY] != '':
                    self._update_page(row[self._ROW_PAGEID_KEY], prop_dict)
                    df.at[index, self._ROW_HASH_KEY] = current_row_hash
                else:
                    page_id = self.create_page(database_ID, prop_dict)
                    df.at[index, self._ROW_PAGEID_KEY] = page_id
                    row[self._ROW_PAGEID_KEY] = page_id
                    df.at[index, self._ROW_HASH_KEY] = self.__row_hash(row)

    def __set_n2p_arg(self, kwargs, field_name, default_value):
        if field_name in kwargs:
            setattr(self, field_name, kwargs[field_name])
            del kwargs[field_name]
        else:
            setattr(self, field_name, default_value)
