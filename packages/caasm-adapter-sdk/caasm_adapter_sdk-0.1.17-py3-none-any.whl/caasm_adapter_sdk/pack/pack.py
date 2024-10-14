import os
import shutil
import subprocess
import tarfile
from datetime import datetime
from typing import Union, List

import yaml
from caasm_service_base.constants.adapter import AdapterRunMode
from rich.console import Console

_BUILD_DIR = "build"
_PACK_DIR = "pack"
_DIST_DIR = "dist"


def _clean():
    shutil.rmtree(_BUILD_DIR, ignore_errors=True)
    shutil.rmtree(_PACK_DIR, ignore_errors=True)
    shutil.rmtree(_DIST_DIR, ignore_errors=True)


def _prepare():
    os.makedirs(_BUILD_DIR, exist_ok=True)
    os.makedirs(_PACK_DIR, exist_ok=True)
    os.makedirs(_DIST_DIR, exist_ok=True)


def _get_file(root_dir, files, ignored_dirs=None, parent_dir=""):
    root_path = os.path.join(root_dir, parent_dir)
    ignored_dirs = ignored_dirs or []
    for name in os.listdir(root_path):
        full_path = os.path.join(root_path, name)
        relative_path = os.path.join(parent_dir, name)
        ignored_dir_found = False
        for ignored_dir in ignored_dirs:
            if relative_path.startswith(ignored_dir):
                ignored_dir_found = True
                break
        if ignored_dir_found:
            continue
        if os.path.isfile(full_path):
            files.append(relative_path)
        else:
            _get_file(root_dir, files, ignored_dirs, os.path.join(parent_dir, name))


def _compress(adapter_name):
    build_path = os.path.join(_BUILD_DIR, adapter_name)
    pack_path = os.path.join(_PACK_DIR, f"{adapter_name}.tar.gz")
    with tarfile.open(pack_path, "w:gz") as tar:
        tar.add(build_path, arcname=".")


def _pack_one(arch: str, adapter_name: str, parent_dir: str = None, build_independent: bool = True):
    console = Console(force_terminal=True)
    console.print(f"[bold green]正在打包适配器：{adapter_name}[/bold green]")
    version = None
    try:
        if parent_dir:
            adapter_path = os.path.join(parent_dir, adapter_name)
        else:
            adapter_path = os.path.join(adapter_name)
        meta_path = os.path.join(adapter_path, "meta.yml")
        with open(meta_path) as fp:
            meta = yaml.safe_load(fp.read())
        version = meta.get("version")
        if not version:
            console.print(f"[bold red]打包适配器出现错误：{adapter_name}[/bold red]")
            console.print("[bold red]meta.yml中不包含有效的版本信息[/bold red]")
            return
        run_mode = meta.get("run_mode") or AdapterRunMode.SHARE.value
        if run_mode == AdapterRunMode.INDEPENDENT.value:
            if not build_independent:
                console.print(f"[bold blue]跳过独立运行适配器打包：{adapter_name}[/bold blue]")
                return
            requirements_path = os.path.join(adapter_path, "requirements.txt")
            extra_requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
            if not os.path.exists(requirements_path):
                console.print(f"[bold red]打包适配器出现错误：{adapter_name}[/bold red]")
                console.print("[bold red]独立运行模式的适配器必须在目录下定义requirements.txt并指定依赖的包[/bold red]")
                return
            #   生成pex运行环境包
            arches = []
            platforms = []
            if arch == "x86_64":
                arches.append("x86_64")
                platforms.append("linux_x86_64-cp-3.8.10-cp38")
            elif arch == "arm64":
                arches.append("aarch64")
                platforms.append("linux_aarch64-cp-3.8.10-cp38")
            elif arch == "both":
                arches.append("x86_64")
                platforms.append("linux_x86_64-cp-3.8.10-cp38")
                arches.append("aarch64")
                platforms.append("linux_aarch64-cp-3.8.10-cp38")
            for index, arch in enumerate(arches):
                platform_name = platforms[index]
                pex_path = os.path.join(_BUILD_DIR, adapter_name, f"{arch}.pex")
                pypi_sources = None
                if os.path.exists("pypi.conf"):
                    with open("pypi.conf") as fp:
                        pypi_sources = fp.readlines()
                if not pypi_sources:
                    pypi_sources = ["https://pypi.tuna.tsinghua.edu.cn/simple"]
                pypi_indices = " ".join(
                    f"--index-url {pypi_source.strip()}"
                    for pypi_source in filter(lambda v: not v.startswith("#"), pypi_sources)
                )
                cmd = f"pex -v -r {requirements_path} -r {extra_requirements_path} -o {pex_path} --platform {platform_name} {pypi_indices} --no-pypi"
                p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if p.returncode != 0:
                    console.print(f"[bold red]打包适配器出现错误：{adapter_name}[/bold red]")
                    console.print("[bold red]无法创建适配器依赖的python运行依赖环境[/bold red]")
                    console.print(f"[bold red]错误信息：{p.stdout} | {p.stderr}[/bold red]")
                    return

        files = []
        _get_file(adapter_path, files, [f"db"])
        for file_name in ["run.py", ".gitignore"]:
            if file_name in files:
                files.remove(file_name)
        for file in files:
            src_file_path = os.path.join(adapter_path, file)
            dst_file_path = os.path.join(_BUILD_DIR, adapter_name, file)
            file_dir_path, _ = os.path.split(dst_file_path)
            os.makedirs(file_dir_path, exist_ok=True)
            shutil.copyfile(src_file_path, dst_file_path)
        _compress(adapter_name)
    finally:
        shutil.rmtree(_BUILD_DIR, ignore_errors=True)
        return adapter_name, version


def _dist(only_one=False, adapter_name=None, version=None, package_name: str = None):
    now = datetime.now()
    if only_one:
        if not package_name:
            package_name = f"{adapter_name}-{version}-adapter_{now.isoformat().replace(':', '_')}.tar.gz"
        dist_file_path = os.path.join(_DIST_DIR, package_name)
    else:
        if not package_name:
            package_name = f"adapter_{now.isoformat().replace(':', '_')}.tar.gz"
        dist_file_path = os.path.join(_DIST_DIR, package_name)
    has_adapter = False
    with tarfile.open(dist_file_path, "w:gz") as tar:
        for adapter_file_name in os.listdir(_PACK_DIR):
            full_path = os.path.join(_PACK_DIR, adapter_file_name)
            if not os.path.isfile(full_path):
                continue
            _, ext_name = os.path.splitext(full_path)
            if ext_name != ".gz":
                continue
            has_adapter = True
            tar.add(full_path, arcname=adapter_file_name)
    if not has_adapter:
        os.remove(dist_file_path)
        console = Console(force_terminal=True)
        console.print(f"[bold red]没有适配器被打包，可能打包出现错误或跳过了独立适配器[/bold red]")


def _pack(arch, adapter_names: Union[str, List[str]] = None, parent_dir: str = None, build_independent: bool = True):
    parent_dir = parent_dir or "."
    #   枚举所有适配器
    if adapter_names is None:
        adapter_names = []
        for entry in os.listdir(parent_dir):
            if os.path.isfile(entry):
                continue
            meta_file_path = os.path.join(parent_dir, entry, "meta.yml")
            if os.path.exists(meta_file_path):
                adapter_names.append(entry)

    if isinstance(adapter_names, str):
        only_one = True
        adapter_name, version = _pack_one(arch, adapter_names, parent_dir, build_independent)
        if adapter_name and version:
            _dist(only_one, adapter_name, version)
    else:
        for adapter_name in adapter_names:
            _pack_one(arch, adapter_name, parent_dir, build_independent)


def pack(arch, adapter_names: Union[str, List[str]] = None, build_independent: bool = True):
    _clean()
    _prepare()
    _pack(arch, adapter_names, build_independent=build_independent)

    if isinstance(adapter_names, List):
        _dist()


def pack_dirs(
    arch, parent_dirs: Union[str, List[str]] = None, package_name: str = None, build_independent: bool = True
):
    if parent_dirs is None:
        parent_dirs = ["."]
    if isinstance(parent_dirs, str):
        parent_dirs = [parent_dirs]

    _clean()
    _prepare()

    for parent_dir in parent_dirs:
        _pack(arch, parent_dir=parent_dir, build_independent=build_independent)
    _dist(package_name=package_name)


if __name__ == "__main__":
    os.chdir("../../")
    pack("x86_64", "weilansec_simple_fetch")
    # pack_dirs("x86_64", ".")
