from weilansec_simple_fetch.clients.client import WeilansecSimpleFetchFetchClient


class BusinessClient(WeilansecSimpleFetchFetchClient):
    URL = "/business"
    METHOD = "post"
