import os.path
import time
from typing import List, Dict, Callable, Mapping

from caasm_persistence_base.handler.storage.base import BasePersistenceHandler
from caasm_persistence_base.handler.storage.manager import storage_manager
from caasm_persistence_base.handler.storage.model.response import (
    CommonResponse,
    DeleteResponse,
    UpdateResponse,
    SaveMultiResponse,
    SaveResponse,
)
from tinydb import TinyDB, Query
from tinydb.queries import QueryInstance

TINYDB_TYPE = "tinydb"


class TinyDBHandler(BasePersistenceHandler):
    def __init__(self, storage_dir: str = None):
        super().__init__()
        self._dbs: Dict[str, TinyDB] = {}
        self._storage_dir = storage_dir or "./db/"

        self._ops = {"$in": self._in, "$gt": self._gt, "$lt": self._lt}

    def _get_db(self, table):
        if table not in self._dbs:
            if not os.path.exists(self._storage_dir):
                os.makedirs(self._storage_dir, exist_ok=True)
            json_path = os.path.join(self._storage_dir, f"{table}.json")
            db = TinyDB(json_path)
            self._dbs[table] = db
        return self._dbs[table]

    @property
    def storage_type(self) -> str:
        return TINYDB_TYPE

    def _gen_id(self):
        return time.time_ns() / 1000

    def save_direct(self, data: Dict, table=None, **kwargs) -> SaveResponse:
        if "_id" not in data:
            data["_id"] = self._gen_id()
        return SaveResponse(True, inserted_id=self._get_db(table).insert(data))

    def save_multi_direct(self, records: List[Dict], table=None, **kwargs) -> SaveMultiResponse:
        for record in records:
            if "_id" not in record:
                record["_id"] = self._gen_id()
        return SaveMultiResponse(True, inserted_ids=self._get_db(table).insert_multiple(records))

    def get_nested(self, data, keys):
        """
        根据提供的路径 keys，动态访问嵌套字典的值。
        :param data: 要查询的嵌套字典
        :param keys: 字符串路径列表，如 ['contact', 'address', 'city']
        :return: 嵌套字段的值，如果路径不存在则返回 None
        """
        for key in keys:
            data = data.get(key)
            if data is None:
                return None
        return data

    def test(self, func: Callable[[Mapping], bool], *args) -> QueryInstance:
        q = Query()
        return q._generate_test(lambda value: func(value, *args), ("test", "", func, args), True)

    def _in(self, keys, value):
        return self.test(lambda v: self.get_nested(v, keys) in value)

    def _gt(self, keys, value):
        return self.test(lambda v: self.get_nested(v, keys) > value)

    def _lt(self, keys, value):
        return self.test(lambda v: self.get_nested(v, keys) < value)

    def dynamic_query(self, path, value):
        keys = path.split(".")
        if isinstance(value, Dict):
            queries = []
            for k, v in value.items():
                op = self._ops.get(k)
                if op:
                    queries.append(op(keys, v))
            return queries
        else:
            func = lambda v: self.get_nested(v, keys) == value
            return [self.test(func)]

    def _build_query(self, condition):
        if not condition:
            return Query()
        queries = []
        for k, v in condition.items():
            queries.extend(self.dynamic_query(k, v))
        final_q = None
        for q in queries:
            if final_q is None:
                final_q = q
            else:
                final_q &= q
        return final_q

    def update_direct(self, condition, values, table=None, **kwargs) -> UpdateResponse:
        return UpdateResponse(True, modified_count=len(self._get_db(table).update(values, condition)))

    def update_multi_direct(self, condition, values, table=None, **kwargs):
        self._get_db(table).update_multiple(values)

    def update_stream_direct(self, mappers: List[Dict], table=None, **kwargs) -> UpdateResponse:
        self._get_db(table).update_multiple(mappers)

    def get_direct(self, condition, fields=None, table=None):
        q = self._build_query(condition)
        return self._get_db(table).get(q)

    def delete_multi(self, condition, table=None):
        q = self._build_query(condition)
        self._get_db(table).remove(q)

    def delete_one(self, condition, table=None) -> DeleteResponse:
        q = self._build_query(condition)
        result = self._get_db(table).remove(q)
        return DeleteResponse(True, deleted_count=len(result))

    def count(self, condition=None, table=None):
        pass

    def find_direct(self, condition=None, fields=None, sort_fields=None, offset=None, limit=None, table=None, **kwargs):
        q = self._build_query(condition)
        result = self._get_db(table).search(q)
        if offset:
            result = result[offset:]
        if limit:
            result = result[:limit]
        return result

    def save_file(self, file_content: bytes, filename=None):
        pass

    def get_file(self, file_id):
        pass

    def check_file_exists(self, file_id):
        pass

    def delete_file(self, file_id):
        pass

    def drop(self, table_name=None) -> CommonResponse:
        db = self._get_db(table_name)
        if db:
            db.drop_table("_default")
        return CommonResponse(True)

    def rename(self, ori_table_name, new_table_name, **kwargs) -> CommonResponse:
        pass


def create_tiny_db(**kwargs):
    pass


storage_manager.register_build_function(TINYDB_TYPE, create_tiny_db)
