#!/usr/bin/env python

import os
import tempfile

from syncup.cmd import Command
from syncup.util import walk_tree, change_root
from syncup.util import copy_file_or_dir, remove_file_or_dir
from syncup.errors import CommandError


class clone(Command):

    def init_options(self):
        self.target = None
        self.lib_prefix = None
        self.data_prefix = None
        self.script_prefix = None
        self.nopyc = True

    def clone_lib(self):
        cached_lib = self.distribution.dist_cache.get('freeze_lib')
        if cached_lib is None:
            raise CommandError, 'please run freeze_lib command before.'

        for name, path in cached_lib:
            dst_pre = self.lib_prefix
            if dst_pre is None:
                dst_pre = os.path.dirname(path)

            dst_pth = os.path.join(dst_pre, name)
            dst_pth = change_root(self.target, dst_pth)

            # TODO: nopyc

            copy_file_or_dir(path, dst_pth, force=True)

    def clone_data(self):
        cached_dat = self.distribution.dist_cache.get('freeze_data')
        if cached_dat is None:
            raise CommandError, 'please run freeze_data command before.'

        for name, path in cached_dat:
            dst_pre = self.data_prefix
            if dst_pre is None:
                dst_pre = os.path.dirname(path)

            dst_pth = os.path.join(dst_pre, name)
            dst_pth = change_root(self.target, dst_pth)

            copy_file_or_dir(path, dst_pth, force=True)

    def clone_script(self):
        cached_bin = self.distribution.dist_cache.get('freeze_script')
        if cached_bin is None:
            raise CommandError, 'please run freeze_script command before.'

        for name, path in cached_bin:
            dst_pre = self.script_prefix
            if dst_pre is None:
                dst_pre = os.path.dirname(path)

            dst_pth = os.path.join(dst_pre, name)
            dst_pth = change_root(self.target, dst_pth)

            copy_file_or_dir(path, dst_pth, force=False)
            os.chmod(dst_pth, 0777)

    def main(self):
        if self.target is None:
            self.target = tempfile.mktemp()

        if os.path.exists(self.target):
            remove_file_or_dir(self.target)
        os.makedirs(self.target)

        self.clone_lib()
        self.clone_data()
        self.clone_script()

        return self.target
