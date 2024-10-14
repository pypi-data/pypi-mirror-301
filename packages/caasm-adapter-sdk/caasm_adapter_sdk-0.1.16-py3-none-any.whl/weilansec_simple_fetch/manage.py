# 从clients包中引用对应的实现类
from weilansec_simple_fetch.clients.business import BusinessClient
from weilansec_simple_fetch.clients.host import HostClient
from weilansec_simple_fetch.clients.owner import OwnerClient
from weilansec_simple_fetch.clients.port import PortClient


class FetchType(object):
    """
    所有对接的API定义，比如接入了auth、device、vul, 那么就需要定义下面三个API
    AUTH = "auth"
    DEVICE = "device"
    VUL = "vul"
    """

    HOST = "host"
    PORT = "port"
    BUSINESS = "business"
    OWNER = "owner"


class Manager(object):
    # key 是ClientType， val是具体的实现类
    _CLIENT_MAPPER = {
        FetchType.HOST: HostClient,
        FetchType.PORT: PortClient,
        FetchType.OWNER: OwnerClient,
        FetchType.BUSINESS: BusinessClient,
    }

    def __init__(self, connection, session=None):
        self._connection = connection
        self._session = session
        self._client_instance_mapper = {}

    def fetch_entities(self, fetch_type, page_index, page_size):
        """
        获取第三方各类实体
        """
        return self._call(fetch_type, page_index=page_index, page_size=page_size)

    def auth(self):
        """
        认证方法
        """
        return False

    def _call(self, fetch_type, *args, **kwargs):
        if fetch_type not in self._client_instance_mapper:
            instance = self._CLIENT_MAPPER[fetch_type](self._connection, self._session)
            self._client_instance_mapper[fetch_type] = instance
        return self._client_instance_mapper[fetch_type].handle(*args, **kwargs)
