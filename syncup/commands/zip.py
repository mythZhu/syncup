#!/usr/bin/env python

import os
import zipfile
import tempfile

from syncup.cmd import Command
from syncup.util import walk_tree, remove_file_or_dir
from syncup.errors import CommandError


class zip(Command):

    def init_options(self):
        self.target = None
        self.lib_prefix = None
        self.data_prefix = None
        self.script_prefix = None
        self.nopyc = True

    def main(self):
        if self.target is None:
            self.target = tempfile.mktemp()

        if os.path.exists(self.target):
            remove_file_or_dir(self.target)

        target_dir = os.path.dirname(self.target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        clone = self.run_command(
                    'clone',
                    lib_prefix=self.lib_prefix,
                    data_prefix=self.data_prefix,
                    script_prefix=self.script_prefix,
                    nopyc=self.nopyc)

        zip = zipfile.ZipFile(self.target, 'w')
        for f in walk_tree(clone):
            if os.path.isdir(f):
                continue
            zip.write(f, os.path.relpath(f, clone))
        zip.close()

        return self.target
