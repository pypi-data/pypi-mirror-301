from caasm_adapter_sdk.scaffold.handlers.base import AdapterAppGenBaseHandler, FileType


class FetchGenHandler(AdapterAppGenBaseHandler):
    @property
    def file_type(self):
        return FileType.PY_MODULE

    @property
    def name(self):
        return "fetch.py"

    def execute_core(self, params):
        super(FetchGenHandler, self).execute_core(params)
        _template_name = "__init__.py"
        _path = self.get_path(_template_name)
        self.write_file(_path, _template_name, params)
