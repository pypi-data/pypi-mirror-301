from caasm_adapter_sdk.scaffold.handlers.base import AdapterAppGenBaseHandler, FileType


class MetaGenHandler(AdapterAppGenBaseHandler):
    @property
    def file_type(self):
        return FileType.YAML

    @property
    def name(self):
        return "meta.yml"
