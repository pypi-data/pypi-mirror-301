from typing import List

from typer import Typer

from caasm_adapter_sdk.commands.pack import pack_adapters
from caasm_adapter_sdk.commands.scaffold import generate_adapter

app = Typer()


@app.command(help="生成适配器框架")
def generate():
    generate_adapter()


@app.command(help="打包适配器供在线更新使用")
def pack():
    pack_adapters()


if __name__ == "__main__":
    app()
