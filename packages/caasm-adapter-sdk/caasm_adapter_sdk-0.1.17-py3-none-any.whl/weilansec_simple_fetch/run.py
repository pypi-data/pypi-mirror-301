from caasm_adapter_sdk.run.adapter_runner import AdapterRunner

adapter_name = "weilansec_simple_fetch"


def init_connection():
    #   这里按照键值对填充适配器参数，如用户名，密码
    connection = {}
    connection["address"] = "http://localhost:10081/"
    #   connection["username"] = "admin"
    #   connection["password"] = "p@ssw0rd"
    return connection


def test_connectivity(connection):
    #   测试网络连通性
    runner = AdapterRunner(adapter_name, connection)
    print(runner.test_connectivity())


def test_auth(connection):
    #   测试认证
    runner = AdapterRunner(adapter_name, connection)
    print(runner.test_auth())


def fetch_single_page(connection, category, fetch_type, page_index=0):
    #   测试抓取指定接口的一个分页数据
    runner = AdapterRunner(adapter_name, connection)
    runner.fetch_single_page(category, fetch_type, page_index)


def fetch_by_fetch_type(connection, category, fetch_type):
    #   测试抓取一个接口所有数据
    runner = AdapterRunner(adapter_name, connection)
    runner.fetch_by_fetch_type(category, fetch_type)


def fetch_by_category(connection, category):
    #   测试抓取一个大类下所有接口数据
    runner = AdapterRunner(adapter_name, connection)
    runner.fetch_by_category(category)


def fetch_all(connection):
    #   测试抓取所有大类数据
    runner = AdapterRunner(adapter_name, connection)
    runner.fetch_all()


def clean_by_fetch_type(connection, category, fetch_type):
    #   测试某一个接口下的清洗工作。注意，如果该接口的清洗工作中存在与其他接口的关联工作，则需要先采集其他关联接口的数据再进行测试
    runner = AdapterRunner(adapter_name, connection)
    runner.clean_by_fetch_type(category, fetch_type)


def clean_by_category(connection, category):
    #   测试某一个大类的所有接口清洗工作。注意，该测试需要先确保所有数据都已正确采集完毕，比如调用fetch_by_category，或者单独执行过每个fetch_type接口下的数据
    runner = AdapterRunner(adapter_name, connection)
    runner.clean_by_category(category)


def fetch_and_clean_by_category(connection, category):
    #   测试抓取一个大类下所有接口数据并进行关联和清洗，形成该大类下最终数据
    runner = AdapterRunner(adapter_name, connection)
    runner.fetch_and_clean_by_category(category)


def fetch_and_clean_all(connection):
    #   测试抓取并关联、清洗所有大类数据，形成完整数据集
    runner = AdapterRunner(adapter_name, connection)
    runner.fetch_and_clean_all()


if __name__ == "__main__":
    #   初始化参数
    connection_ = init_connection()

    #   测试连通性
    #   test_connectivity(connection_)

    #   测试认证
    #   test_auth(connection_)

    #   测试抓取和关联清洗数据
    #   使用上面fetch_*函数完成测试抓取和关联、清洗工作
    #   建议从fetch_single_page和fetch_by_fetch_type开始测试单个接口的可用性，再调用clean_by_fetch_type测试每一个大类下关联工作

    fetch_and_clean_all(connection_)

    pass
