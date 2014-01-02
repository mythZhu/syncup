#!/usr/bin/env python

import os
import sys

from syncup.cmd import Command
from syncup.util import change_root
from syncup.errors import CommandError


class freeze_lib(Command):

    def init_options(self):
        self.paths = None
        self.root = None

    def py_paths(self):
        if self.paths:
            select_paths = self.paths
        else:
            select_paths = sys.path

        if self.root:
            select_paths = [ change_root(self.root, p) for p in select_paths ]

        return select_paths

    def find_package(self, package):
        for path in self.py_paths():
            full = os.path.join(path, package)
            init_py = os.path.join(full, '__init__.py')
            if os.path.isdir(full) and os.path.isfile(init_py):
                return package, full
        else:
            raise CommandError, 'No package with the name %s found' % package

    def find_module(self, module):
        for path in self.py_paths():
            full = os.path.join(path, module + '.py')
            if os.path.isfile(full):
                return module, full
        else:
            raise CommandError, 'No module with the name %s found' % package

    def main(self):
        modules = []
        for mod in self.distribution.py_modules:
            modules.append(self.find_module(mod))

        packages = []
        for pkg in self.distribution.packages:
            packages.append(self.find_package(pkg))

        output = []
        output.extend(modules)
        output.extend(packages)

        return output
