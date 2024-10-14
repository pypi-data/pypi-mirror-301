from caasm_adapter_sdk.scaffold.handlers.base import AdapterAppGenBaseHandler, FileType


class LogoHandler(AdapterAppGenBaseHandler):
    @property
    def file_type(self):
        return FileType.CP

    @property
    def name(self):
        return "logo.png"
