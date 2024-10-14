from weilansec_simple_fetch.clients.client import WeilansecSimpleFetchFetchClient


class HostClient(WeilansecSimpleFetchFetchClient):
    URL = "/host"
    METHOD = "post"
