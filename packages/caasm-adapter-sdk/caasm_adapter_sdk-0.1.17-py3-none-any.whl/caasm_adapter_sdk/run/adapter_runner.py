import inspect
import os.path
from typing import Dict

import requests
import yaml
from caasm_tool.util import load_module, load_entry, extract

from caasm_adapter_sdk.run.fetch_handler import FetchHandler
from caasm_adapter_sdk.run.service.fetch_service_local import fetch_service_local
from caasm_config.config import caasm_config


class AdapterRunner:
    def __init__(self, adapter_name, connection: Dict):
        caasm_config.install()
        self._adapter_name = adapter_name
        self._root = self._calculate_root(adapter_name)
        self._meta = self._load_meta()
        self._connection = connection

    @staticmethod
    def _calculate_root(adapter_name):
        module_file_path = inspect.getfile(load_module(adapter_name))
        return os.path.dirname(module_file_path)

    def _load_meta(self):
        meta_file_path = os.path.join(self._root, "meta.yml")
        with open(meta_file_path) as fp:
            return yaml.safe_load(fp.read())

    def _create_handler(self, category):
        handler = FetchHandler(category, self._adapter_name, fetch_service_local, self._meta)
        handler.set_connection(self._connection)
        handler.initialize()
        return handler

    def test_connectivity(self):
        key = "test_connection_point"
        if key not in self._meta or not self._meta[key]:
            raise Exception("未定义有效的测试连通性入口点")
        entry = load_entry(key)
        context = {}
        return bool(entry(self._connection, requests.Session(), context))

    def test_auth(self):
        key = "test_auth_point"
        if key not in self._meta or not self._meta[key]:
            raise Exception("未定义有效的测试认证入口点")
        entry = load_entry(key)
        return bool(entry(self._connection, requests.Session()))

    def _get_fetch_type_mapper(self):
        category_mapping = extract(self._meta, "fetch_setting.fetch_type_mapper")
        if not category_mapping:
            raise ValueError("在meta.yml文件中未定义有效的fetch_setting.fetch_type_mapper字段")
        return category_mapping

    def _drop(self, category):
        fetch_service_local.drop(f"{self._adapter_name}_{category}")

    def fetch_single_page(self, category, fetch_type, page_index=0):
        self._drop(category)
        handler = self._create_handler(category)
        context = {}
        handler.fetch(fetch_type, page_index, context)

    def fetch_by_fetch_type(self, category, fetch_type):
        self._drop(category)
        handler = self._create_handler(category)
        handler.fetch_by_fetch_type(fetch_type)

    def fetch_by_category(self, category):
        self._drop(category)
        category_mapping = self._get_fetch_type_mapper()
        if category not in category_mapping:
            raise ValueError("在meta.yml文件中fetch_setting.fetch_type_mapper字段不包含指定的category采集类型")
        handler = self._create_handler(category)
        handler.fetch_all()

    def fetch_all(self):
        category_mapping = self._get_fetch_type_mapper()
        for category in category_mapping.keys():
            self._drop(category)
            self.fetch_by_category(category)

    def clean_by_fetch_type(self, category, fetch_type):
        handler = self._create_handler(category)
        handler.clean_by_fetch_type(fetch_type)

    def clean_by_category(self, category):
        handler = self._create_handler(category)
        handler.clean_all()

    def fetch_and_clean_by_category(self, category):
        self._drop(category)
        category_mapping = self._get_fetch_type_mapper()
        if category not in category_mapping:
            raise ValueError("在meta.yml文件中fetch_setting.fetch_type_mapper字段不包含指定的category采集类型")
        handler = self._create_handler(category)
        handler.handle()

    def fetch_and_clean_all(self):
        category_mapping = self._get_fetch_type_mapper()
        for category, fetch_types in category_mapping.items():
            self._drop(category)
            handler = self._create_handler(category)
            handler.handle()


if __name__ == "__main__":
    print(inspect.getfile(load_module("sangfor_ad")))
