from caasm_adapter.fetcher.cleaners.base import FetchBaseCleaner
<%!
    import re

    def underline2hump(underline_str):
        sub = re.sub(r"(_\w)", lambda x: x.group(1)[1].upper(), underline_str)
        return sub[0].upper() + sub[1:]
%>

class ${underline2hump(adapter_name)}StandardCleaner(FetchBaseCleaner):
    """
    标准的清洗流程，数据不需要重新聚合处理，适合可以直接拿到业务信息的流程
    """

    def clean_single(self, detail):
        """
        填充业务逻辑，如果返回None，{}, False, 0（python中的空，则代表不清洗该条记录）
        """
        return {}
