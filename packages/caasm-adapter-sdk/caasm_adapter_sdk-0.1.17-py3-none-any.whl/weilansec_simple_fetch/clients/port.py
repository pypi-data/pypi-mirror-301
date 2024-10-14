from weilansec_simple_fetch.clients.client import WeilansecSimpleFetchFetchClient


class PortClient(WeilansecSimpleFetchFetchClient):
    URL = "/port"
    METHOD = "post"
