import os
import shutil

from mako.template import Template

from caasm_adapter_sdk.scaffold.constant import ROOT_PATH


class FileType(object):
    PY_MODULE = "py_module"
    PY_PACKAGE = "py_package"
    YAML = "yaml"
    FOLDER = "folder"
    CP = "cp"


class AdapterAppGenBaseHandler(object):
    def __init__(self, adapter_path):
        self._adapter_path = adapter_path
        self._template_root_path = os.path.join(ROOT_PATH, "templates")

    def execute(self, params):
        self._cp_file()
        self._gen_folder()
        self.execute_core(params)

    def _cp_file(self):
        if self.file_type != FileType.CP:
            return
        src_path = os.path.join(self._template_root_path, f"{self.name}")
        dst_path = self.get_current_path()
        if os.path.exists(dst_path):
            os.remove(dst_path)
        shutil.copy(src_path, dst_path)

    def execute_core(self, params):
        if self.file_type in (FileType.FOLDER, FileType.PY_PACKAGE, FileType.CP):
            return
        _path = self.get_current_path()
        self.write_file(_path, self.name, template_params=params)

    def _gen_folder(self):
        if self.file_type not in (FileType.FOLDER, FileType.PY_PACKAGE):
            return

        _path = self.get_current_path()
        os.makedirs(_path)

        if self.file_type == FileType.PY_PACKAGE:
            self.write_file(self.get_current_path("__init__.py"))

    @property
    def file_type(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    def write_current_file(self, file_name, template_params):
        _path = self.get_current_path(file_name)
        self.write_file(_path, file_name, template_params)

    def write_file(self, file_path, template_name=None, template_params=None):
        content = ""
        if template_name:
            template_params = template_params or {}
            content = self.get_render_content(template_name, **template_params)
        with open(file_path, "w") as fd:
            fd.write(content)

    def get_path(self, name, *args):
        return os.path.join(self._adapter_path, name, *args)

    def get_current_path(self, *args):
        return self.get_path(self.name, *args)

    def get_render_content(self, name, **kwargs):
        _template_path = os.path.join(self._template_root_path, f"{name}.tpl")
        with open(_template_path, "r") as fd:
            _content_define = fd.read()
            _template = Template(_content_define)
        return _template.render(**kwargs)
