from weilansec_simple_fetch.clients.client import WeilansecSimpleFetchFetchClient


class OwnerClient(WeilansecSimpleFetchFetchClient):
    URL = "/owner"
    METHOD = "post"
