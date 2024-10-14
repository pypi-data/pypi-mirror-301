from caasm_adapter_sdk.scaffold.handlers.base import AdapterAppGenBaseHandler, FileType


class FabricGenHandler(AdapterAppGenBaseHandler):
    @property
    def file_type(self):
        return FileType.PY_MODULE

    @property
    def name(self):
        return "fabric.py"
