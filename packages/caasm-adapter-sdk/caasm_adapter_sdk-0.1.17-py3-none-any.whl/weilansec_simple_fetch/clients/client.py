from abc import ABC

from caasm_adapter_base.util.client import FetchJsonResultClient


class WeilansecSimpleFetchFetchClient(FetchJsonResultClient, ABC):
    @property
    def data_key_name(self):
        return "data"

    @property
    def success_flag(self):
        return 0

    @property
    def flag_key_name(self):
        return "code"

    def build_request_json(self, *args, **kwargs):
        return kwargs
