from caasm_adapter_sdk.scaffold.handlers.base import AdapterAppGenBaseHandler, FileType


class CleanerGenHandler(AdapterAppGenBaseHandler):
    @property
    def file_type(self):
        return FileType.PY_PACKAGE

    @property
    def name(self):
        return "cleaners"

    def execute_core(self, params):
        if params.get("standard_clean"):
            self.write_current_file("clean_standard.py", params)

        if params.get("total_clean"):
            self.write_current_file("clean_total.py", params)
