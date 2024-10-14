from abc import ABC

from caasm_adapter_base.util.client import FetchJsonResultClient
<%!
    import re

    def underline2hump(underline_str):
        sub = re.sub(r"(_\w)", lambda x: x.group(1)[1].upper(), underline_str)
        return sub[0].upper() + sub[1:]
%>

class ${underline2hump(adapter_name)}FetchClient(FetchJsonResultClient, ABC):
    pass