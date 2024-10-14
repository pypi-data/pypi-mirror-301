from caasm_adapter_base.fetcher.fetch_handler_base import BaseFetchHandler
from caasm_adapter_base.fetcher.fetch_service_base import BaseFetchService
from caasm_adapter_base.sdk.adapter_fetch import BaseAdapterFetchSdk
from caasm_service_base.schema.runtime import adapter_schema
from caasm_tool.util import load_class

from caasm_adapter_sdk.run.service.fetch_service_local import fetch_service_local


class FetchHandler(BaseFetchHandler):
    def __init__(self, category, adapter_name, fetch_service: BaseFetchService, _meta_content):
        super().__init__(category, adapter_name, fetch_service, BaseAdapterFetchSdk(fetch_service_local))
        self._meta_content = _meta_content

    def _load_adapter(self):
        return adapter_schema.load(self._meta_content)

    def _load_fetch_record(self):
        self._table_name = f"{self.adapter_name}_{self.category}"

    def _load_cleaner(self, clean_meta_point, fetch_type):
        return load_class(clean_meta_point)(
            self.adapter_name,
            None,
            self.index,
            self.category,
            fetch_type,
            self._fetch_sdk,
            self._fetch_service,
        )
