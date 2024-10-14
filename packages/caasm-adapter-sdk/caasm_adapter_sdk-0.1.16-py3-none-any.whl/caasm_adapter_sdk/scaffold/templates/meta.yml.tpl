# 需要根据实际情况进行修改的是必须要改的，具体怎么改参考https://e.gitee.com/weilansec/projects/433637/docs?directory=1188256&page=1&program_id=433637&scope=root&sub_id=7656957
# 需要确认的是可能不改，根据实际业务情况决定

name: ${adapter_name}
display_name: ${adapter_name_cn}
description: "" # 需要根据实际情况进行修改
type: ${product_type}
company: ${vendor_cn}
logo: "logo.png" # 需要根据实际情况进行修改
run_mode: ${run_mode}
builtin: false # 是否为内建适配器，如果是官方开发通用适配器，此处为true；如果为定制开发或由客户自行开发，此处为false

version: "0.1"
priority: 1  # 需要确认
properties: [] # 需要根据实际情况进行修改

connection: # 需要根据实际情况进行修改
  - name: address
    type: url
    required: true
    display_name: "地址"
    description: "地址信息"
    validate_rules:
      - name: reg
        error_hint: "地址信息无效，请输入以http或者https开头的地址信息"
        setting:
          reg: '^((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})*(/[a-zA-Z0-9\&%_\./-~-#]*)?$'

  # 需要按照address的样例补全业务所需的剩余参数（比如username、password）

fetch_setting:
  type: disposable
  point: "${adapter_name}.fetch:fetch"
  context_point: "${adapter_name}.fetch:build_query_context"
  is_need_test_service: true
  test_connection_point: "${adapter_name}.fetch:test_connectivity"
  test_auth_point: "${adapter_name}.fetch:test_auth"
  finish_point: "${adapter_name}.fetch:finish"
  count_point: "" # 需要确认
  mode: "default" # 需要确认
  size: 100 # 需要确认
  fetch_type_mapper: {} # 需要根据实际情况进行修改
  cleaner_mapper: {}  # 需要确认

merge_setting:
  size: 100  # 需要确认
  setting: {} # 需要根据实际情况进行修改

convert_setting:
  size: 100 # 需要确认
  before_executor_mapper: {}
  executor_mapper: {}

fabric_setting:
  choose_point_mapper:
    asset: "${adapter_name}.fabric:choose_new_record" # 需要确认