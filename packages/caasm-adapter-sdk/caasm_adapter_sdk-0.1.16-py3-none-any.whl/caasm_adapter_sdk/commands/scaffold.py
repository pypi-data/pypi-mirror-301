import os.path
import re

from caasm_service_base.constants.adapter import AdapterRunMode
from rich.console import Console

from caasm_adapter_sdk.commands.utils import input_str, input_enum, input_confirm
from caasm_adapter_sdk.scaffold.manager import AdapterAppGenManager

_NAME_REGEX = re.compile(r"[a-z][a-z_]*[a-z]|[a-z]")

_ADAPTER_TYPES = [
    "主机防护",
    "终端防护",
    "终端审计",
    "容器安全",
    "流量检测",
    "互联网测绘",
    "内网资产测绘",
    "堡垒机",
    "脆弱性评估",
    "云平台",
    "云管平台",
    "物联网安全",
    "情报",
    "虚拟化平台",
    "CMDB",
    "API",
    "安全测试",
    "蜜罐",
    "网络配置",
    "防火墙",
    "账户",
    "IAM",
    "零信任",
    "应用",
    "文件导入",
    "数据库导入",
    "Kafka导入",
]

_RUN_MODES = {
    "共享模式": (AdapterRunMode.SHARE.value, "该适配器共享平台Python运行时，适用于当适配器未使用平台未安装的第三方库时。使用独立运行模式打出的包较小。"),
    "独立模式": (AdapterRunMode.INDEPENDENT.value, "该适配器独享Python运行时，适用于当适配器使用了平台未安装的第三方库时。使用独立运行模式打出的包较大。"),
}


def generate_adapter():
    console = Console(force_terminal=True)
    console.print("欢迎使用[bold violet]未岚科技CAASM平台[/bold violet]适配器脚手架，请根据向导完成适配器基本框架创建")
    params = {}

    vendor = input_str(
        "请输入[bold green]适配器厂商英文名称[/bold green]，如[bold blue]sangfor[/bold blue]，[bold blue]db_app_security[/bold blue]\n[bold violet]必须以小写字母开头和结尾，仅包含小写字母及下划线[/bold violet]\n[bold violet]长度不超过32[/bold violet]",
        32,
        regex=_NAME_REGEX,
    )
    vendor_cn = input_str(
        "请输入[bold green]适配器厂商显示名称[/bold green]，如[bold blue]深信服[/bold blue]，[bold blue]安恒[/bold blue]\n[bold violet]长度不超过32[/bold violet]",
        32,
    )
    product = input_str(
        "请输入要对接的[bold green]产品或平台英文名称[/bold green]，如[bold blue]ad[/bold blue]，[bold blue]scanner[/bold blue]\n[bold violet]必须以小写字母开头和结尾，仅包含小写字母及下划线，长度不超过32[/bold violet]",
        32,
    )
    product_cn = input_str(
        "请输入[bold green]产品或平台显示名称[/bold green]，如[bold blue]AD[/bold blue]，[bold blue]明鉴[/bold blue]\n[bold violet]长度不超过32[/bold violet]",
        32,
    )
    product_type = input_enum("请选择[bold green]对接产品所属类别[/bold green]\n", _ADAPTER_TYPES)
    run_mode = input_enum("请选择[bold green]适配器运行模式[/bold green]\n", _RUN_MODES)
    path = input_str("请输入[bold green]适配器框架目录创建路径[/bold green]", 1024, required=False, default="当前目录")
    if path == "当前目录":
        path = "./"
    adapter_name = f"{vendor}_{product}"
    params["adapter_name"] = adapter_name
    params["vendor_cn"] = vendor_cn
    params["adapter_name_cn"] = product_cn
    params["product_type"] = product_type
    params["run_mode"] = run_mode
    if os.path.exists(os.path.join(path, adapter_name)):
        force_save_flag = input_confirm("适配器已存在，是否覆盖？[bold red]如果选择覆盖则会清空现有目录和文件！[/bold red]")
    else:
        force_save_flag = None
    console.print("正在生成适配器框架......")
    manager = AdapterAppGenManager(save_path=path, adapter_name=adapter_name, force_save_flag=force_save_flag)

    with console:
        try:
            manager.execute(params)
        except Exception as e:
            console.print(f"[bold red]{str(e)}[/bold red]")
            return

    console.print("生成完成，请根据开发文档完成后续工作")
