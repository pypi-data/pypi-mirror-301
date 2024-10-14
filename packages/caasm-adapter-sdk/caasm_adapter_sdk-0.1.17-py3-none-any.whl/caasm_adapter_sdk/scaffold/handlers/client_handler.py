from caasm_adapter_sdk.scaffold.handlers.base import AdapterAppGenBaseHandler, FileType


class ClientGenHandler(AdapterAppGenBaseHandler):
    @property
    def file_type(self):
        return FileType.PY_PACKAGE

    @property
    def name(self):
        return "clients"

    def execute_core(self, params):
        super(ClientGenHandler, self).execute_core(params)
        self.write_current_file("client.py", params)
