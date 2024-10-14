from caasm_adapter_base.fetcher.cleaners.base import FetchTotalBaseCleaner
<%!
    import re

    def underline2hump(underline_str):
        sub = re.sub(r"(_\w)", lambda x: x.group(1)[1].upper(), underline_str)
        return sub[0].upper() + sub[1:]
%>

class ${underline2hump(adapter_name)}TotalCleaner(FetchTotalBaseCleaner):
    """
    数据需要重新聚合的清洗流程
    """

    def build_common(self, biz_records):
        return biz_records
