from core import Daemon
from core import Log

import os
import subprocess

class Module:
    def start(self):
        self.__print_pending_change()
        self.__scan_modules()

    def __print_pending_change(self, module_name=''):
        path = Daemon.ROOT_PATH

        if module_name:
            path = '%smodules/%s/' % (path, module_name)

        result = subprocess.getoutput('cd "%s" && git status' % path)

        if not 'nothing to commit' in result:
            type =  '"%s" module' % module_name if module_name else 'core'
            Log.debug('change in %s: %s' % (type, result))

    def __scan_modules(self):
        dir_list = sorted(os.listdir(Daemon.MODULES_PATH))

        for module_name in dir_list:
            dir_path = '%s%s/' % (Daemon.MODULES_PATH, module_name)

            if '__pycache__' in module_name or not os.path.isdir(dir_path):
                continue

            self.__print_pending_change(module_name)

