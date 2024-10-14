import re
from typing import List, Union, Dict, Tuple

from rich.console import Console

_NUMBER_REGEX = re.compile(r"\d+")


def input_str(prompt, length, required=True, default=None, regex=None):
    console = Console(force_terminal=True)
    while True:
        console.print()
        prompt_ = prompt
        if required:
            prompt_ += "\n[bold violet]输入值不能为空[/bold violet]"
        if default:
            value = console.input(
                prompt_ + f"\n[bold violet]直接按回车使用默认值[/bold violet][[bold blue]{default}[/bold blue]]: "
            )
        else:
            value = console.input(prompt_ + "\n: ")
        if not value:
            if required:
                console.print("[bold red]不能输入空值，请重新输入[/bold red]")
                continue
            else:
                value = default
                break
        if regex:
            if not regex.fullmatch(value):
                console.print("[bold red]输入值格式不符合要求，请重新输入[/bold red]")
                continue
        if len(value) > length:
            console.print("[bold red]输入值长度不符合要求[/bold red]")
            continue
        break
    return value


def input_enum(prompt, enums: Union[List[str], Dict[str, Tuple[str, str]]], required=True):
    console = Console(force_terminal=True)
    index = 1
    prompts = []
    prompt_ = prompt
    if isinstance(enums, List):
        for e in enums:
            prompts.append(f"{index}. [bold blue]{e}[/bold blue]")
            index += 1
    else:
        for k, v in enums.items():
            prompts.append(f"{index}. [bold blue]{k}[/bold blue]：[bold green]{v[1]}[/bold green]")
            index += 1
    prompt_ += "\n".join(prompts)
    while True:
        value = input_str(prompt_, 2, required=required, regex=_NUMBER_REGEX)
        try:
            value = int(value)
        except ValueError:
            console.print("[bold red]请输入正确的类型序号[/bold red]")
            continue
        finally:
            if value > len(enums):
                console.print("[bold red]请输入正确的类型序号[/bold red]")
                continue
            break
    if isinstance(enums, List):
        return enums[value - 1]
    else:
        return enums[list(enums.keys())[value - 1]][0]


def input_confirm(prompt):
    console = Console(force_terminal=True)
    prompt_ = prompt
    prompt_ += '[bold violet]确定输入"y"/取消输入"n"[/bold violet]\n: '
    while True:
        selection = console.input(prompt_)
        if selection not in {"y", "n"}:
            console.print("[bold red]请输入正确的选项[/bold red]")
            continue
        break
    return selection
