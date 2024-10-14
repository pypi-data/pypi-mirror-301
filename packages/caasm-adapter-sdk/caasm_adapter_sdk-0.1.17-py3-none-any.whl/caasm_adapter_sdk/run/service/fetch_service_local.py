from typing import List, Dict

from caasm_adapter_base.fetcher.fetch_service_base import BaseFetchService

from caasm_adapter_sdk.run.persistence.handler.tiny_db import TinyDBHandler


class FetchServiceLocal(BaseFetchService, TinyDBHandler):
    @classmethod
    def build_fetch_data_condition(cls, fetch_type=None, data_ids=None):
        condition = {}
        if fetch_type:
            condition["internal.fetch_type"] = fetch_type

        if data_ids:
            condition["_id"] = {"$in": data_ids}

        return condition

    @classmethod
    def build_fetch_data_table(cls, adapter_name, adapter_instance_id, fetch_type, index):
        return f"{adapter_name}_{fetch_type}"

    def delete_fetch_data(self, table, data_ids):
        pass

    def delete_fetch_data_by_fetch_type(self, table, fetch_type):
        pass

    def save(self, records: List[Dict], table=None, **kwargs):
        pass

    def update(self, mappers: List[Dict], table=None, simple_values=True, **kwargs):
        pass

    def drop(self, table_name=None):
        pass

    def rename(self, ori_table_name, new_table_name, **kwargs):
        pass


fetch_service_local = FetchServiceLocal()
