import os
import shutil

from caasm_adapter_sdk.scaffold.handlers.clean_handler import CleanerGenHandler
from caasm_adapter_sdk.scaffold.handlers.client_handler import ClientGenHandler
from caasm_adapter_sdk.scaffold.handlers.demo_handler import DemoGenHandler
from caasm_adapter_sdk.scaffold.handlers.fabric_handler import FabricGenHandler
from caasm_adapter_sdk.scaffold.handlers.fetch_handler import FetchGenHandler
from caasm_adapter_sdk.scaffold.handlers.gitignore_handler import GitIgnoreHandler
from caasm_adapter_sdk.scaffold.handlers.logo_handler import LogoHandler
from caasm_adapter_sdk.scaffold.handlers.manage_handler import ManageGenHandler
from caasm_adapter_sdk.scaffold.handlers.meta_handler import MetaGenHandler
from caasm_adapter_sdk.scaffold.handlers.release_notes import ReleaseNotesHandler
from caasm_adapter_sdk.scaffold.handlers.rule_handler import RuleGenHandler
from caasm_adapter_sdk.scaffold.handlers.run_handler import RunGenHandler


class AdapterAppGenManager(object):
    _handlers = [
        ClientGenHandler,
        CleanerGenHandler,
        RuleGenHandler,
        DemoGenHandler,
        FabricGenHandler,
        FetchGenHandler,
        ManageGenHandler,
        MetaGenHandler,
        LogoHandler,
        RunGenHandler,
        GitIgnoreHandler,
        ReleaseNotesHandler,
    ]

    def __init__(self, save_path, adapter_name, force_save_flag=False):
        self._save_path = save_path
        self._adapter_name = adapter_name
        self._force_save_flag = force_save_flag

        self.__adapter_path = os.path.join(self._save_path, self._adapter_name)
        self.__handler_instances = []

        self.__init_handler_instances()

    def execute(self, params):
        self._execute_check()
        self._execute_core(params)

    def _execute_check(self):
        if not os.access(self._save_path, os.W_OK):
            return Exception(f"适配器路径({self._save_path})无写入权限")

        if self._force_save_flag:
            shutil.rmtree(self.__adapter_path) if os.path.exists(self.__adapter_path) else ...
        else:
            if os.access(self.__adapter_path, os.F_OK):
                raise Exception(f"适配器路径({self.__adapter_path})已经存在")

    def _execute_core(self, params):
        for _handler_instance in self.__handler_instances:
            _name = _handler_instance.name
            _handler_instance.execute(params)

    def __init_handler_instances(self):
        for _handler_define in self._handlers:
            _handler_instance = _handler_define(self.__adapter_path)
            self.__handler_instances.append(_handler_instance)
