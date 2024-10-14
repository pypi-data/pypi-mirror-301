from caasm_adapter_base.fetcher.cleaners.base import FetchTotalBaseCleaner


class HostCleaner(FetchTotalBaseCleaner):
    def build_common(self, biz_records):
        for record in biz_records:
            record["cleaned"] = True
        return biz_records
