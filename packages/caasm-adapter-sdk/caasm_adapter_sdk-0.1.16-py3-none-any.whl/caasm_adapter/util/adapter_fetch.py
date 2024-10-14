import os.path

from caasm_adapter_base.util.adapter_fetch import BaseAdapterFetchUtil
from nanoid import generate

from caasm_config.config import caasm_config


class AdapterFetchUtil(BaseAdapterFetchUtil):
    def get_driver_path(self):
        return caasm_config.CHROME_DRIVER_PATH

    def save_file(self, file_content: bytes, filename=None):
        file_id = generate()
        file_path = os.path.join("files", file_id)
        with open(file_path, "wb") as fp:
            fp.write(file_content)
        return file_id

    def get_file(self, file_id):
        path = os.path.join("files", file_id)
        if not os.path.exists(path):
            raise FileNotFoundError()
        with open(path, "rb") as fp:
            return fp.read()

    def check_file_exists(self, file_id):
        path = os.path.join("files", file_id)
        return os.path.exists(path)

    def delete_file(self, file_id):
        path = os.path.join("files", file_id)
        os.remove(path)


fetch_util = AdapterFetchUtil()
