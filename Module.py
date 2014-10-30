from core import Daemon
from core import Log

from circuits import Component
import os
import subprocess

class Module(Component):
    def started(self, component):
        self.__print_pending_change()
        self.__scan_modules()

    def __print_pending_change(self, module_name=''):
        path = Daemon.ROOT_PATH

        if module_name:
            path = os.path.join(path, 'modules', module_name)

        result = subprocess.getoutput('cd "%s" && git status' % path)

        if not 'nothing to commit' in result:
            type =  '"%s" module' % module_name if module_name else 'core'
            Log.debug('change in %s: %s' % (type, result))

    def __scan_modules(self):
        dir_list = sorted(os.listdir(Daemon.MODULES_PATH))

        for module_name in dir_list:
            dir_path = os.path.join(Daemon.MODULES_PATH, module_name)

            if '__pycache__' in module_name or not os.path.isdir(dir_path):
                continue

            if not os.path.isdir(os.path.join(dir_path, '.git')):
                Log.debug('Not git repository: %s' % dir_path)
                continue

            self.__print_pending_change(module_name)

