from rich.console import Console

from caasm_adapter_sdk.commands.utils import input_enum, input_str
from caasm_adapter_sdk.pack.pack import pack

_ARCHES = {
    "x86_64": ("x86_64", "64位x86架构，Intel，AMD，海光均属于该架构"),
    "aarch64": ("aarch64", "64位ARM架构，华为鲲鹏等属于该架构"),
    "both": ("both", "同时打包x86_64和arm64架构，打包时间会更长"),
}


def pack_adapters():
    console = Console(force_terminal=True)
    console.print("欢迎使用[bold violet]未岚科技CAASM平台[/bold violet]适配器打包程序，请根据向导完成适配器打包")
    params = {}

    arch = input_enum("请选择[bold green]打包的CPU架构[/bold green]\n", _ARCHES)
    params["arch"] = arch

    adapters_str = input_str("请输入要打包的适配器英文名称（即目录名），多个适配器以逗号分割，直接回车则打包所有适配器", 10240, False)
    if adapters_str:
        adapter_names = adapters_str.split(",")
    else:
        adapter_names = None
    params["adapter_names"] = adapter_names or None

    pack(**params)
