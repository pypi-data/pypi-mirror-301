from weilansec_simple_fetch.manage import Manager
from caasm_adapter.util.adapter_fetch import fetch_util


def build_query_context(connection, session, fetch_type, *args, **kwargs):
    #   创建额外上下文信息
    return {}


def _build_manager(connection, session):
    return Manager(connection, session)


def test_connectivity(connection, session):
    #   测试连通性
    #   connection：对应界面创建适配器时应输入的各项参数，如用户名、密码、token、url、ip等
    pass


def test_auth(connection, session):
    #   测试认证
    #   connection：对应界面创建适配器时应输入的各项参数，如用户名、密码、token、url、ip等
    _build_manager(connection, session).auth()


def fetch(connection, fetch_type, page_index=0, page_size=1, session=None, context=None, **kwargs):
    #   采集原始实体数据
    #   connection：对应界面创建适配器时应输入的各项参数，如用户名、密码、token、url、ip等
    #   fetch_type: 采集类型，一般对应对接的第三方平台的接口。由于可能需要对不同接口数据进行关联整合，因此不一定与CAASM平台的资产类型对应
    #   page_index: 当前采集的分页序号，一般对应对接的第三方平台的分页机制。默认从0开始
    #   page_size: 当前采集的分页大小，一般对应对接的第三方平台的分页机制
    #   session: 公用的requests的会话，如果对接的第三方平台采用http协议接口，同时需要在不同接口调用时需要维持会话及会话中的header、cookie等信息时使用
    #   context: 适配器内部维持的上下文字典，用于存放在不同接口调用对象中共享的各类变量、对象等

    _manager = _build_manager(connection, session)
    records = _manager.fetch_entities(fetch_type, page_index=page_index, page_size=page_size)
    result = fetch_util.build_asset(records, fetch_type)
    return fetch_util.return_success(result)


def finish(connection=None, session=None, context=None):
    pass
