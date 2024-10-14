from caasm_adapter_sdk.scaffold.handlers.base import AdapterAppGenBaseHandler, FileType


class ReleaseNotesHandler(AdapterAppGenBaseHandler):
    @property
    def file_type(self):
        return FileType.CP

    @property
    def name(self):
        return "release_notes.md"
