from caasm_adapter_sdk.scaffold.handlers.base import AdapterAppGenBaseHandler, FileType


class DemoGenHandler(AdapterAppGenBaseHandler):
    @property
    def file_type(self):
        return FileType.FOLDER

    @property
    def name(self):
        return "demos"
