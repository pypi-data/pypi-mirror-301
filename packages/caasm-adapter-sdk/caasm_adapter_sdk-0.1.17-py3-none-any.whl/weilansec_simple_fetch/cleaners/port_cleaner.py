from caasm_adapter_base.fetcher.cleaners.base import FetchLinkBaseCleaner

from weilansec_simple_fetch.manage import FetchType


class PortCleaner(FetchLinkBaseCleaner):
    @property
    def main_fetch_type(self):
        return "port"

    @property
    def main_field(self):
        return "ip"

    @property
    def link_fetch_type(self):
        return FetchType.HOST
