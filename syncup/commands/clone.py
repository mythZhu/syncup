#!/usr/bin/env python

import os
import tempfile

from syncup.cmd import Command
from syncup.util import walk_tree, change_root, real_prefix
from syncup.util import copy_file_or_dir, remove_file_or_dir
from syncup.errors import CommandError


class clone(Command):

    def init_options(self):
        self.target = None
        self.lib_prefix = None
        self.data_prefix = None
        self.script_prefix = None
        self.nopyc = True

    def gen_dst_path(self, name, full, root, prefix):
        dst_prefix = self.lib_prefix or real_prefix(prefix)
        dst_base = os.path.basename(full)
        dst_base = os.path.join(os.path.dirname(name), dst_base)
        dst_full = os.path.join(dst_prefix, dst_base)
        dst_full = change_root(self.target, dst_full)

        return dst_full

    def clone_lib(self):
        cached_lib = self.distribution.dist_cache.get('freeze_lib')
        if cached_lib is None:
            raise CommandError, 'please run freeze_lib command before.'

        for (name, full, root, prefix) in cached_lib:
            dst_full = self.gen_dst_path(name, full, root, prefix)

            copy_file_or_dir(full, dst_full, ignores=('*.pyc', '*.pyo'))

    def clone_data(self):
        cached_dat = self.distribution.dist_cache.get('freeze_data')
        if cached_dat is None:
            raise CommandError, 'please run freeze_data command before.'

        for (name, full, root, prefix) in cached_dat:
            dst_full = self.gen_dst_path(name, full, root, prefix)

            copy_file_or_dir(full, dst_full)

    def clone_script(self):
        cached_bin = self.distribution.dist_cache.get('freeze_script')
        if cached_bin is None:
            raise CommandError, 'please run freeze_script command before.'

        for (name, full, root, prefix) in cached_bin:
            dst_full = self.gen_dst_path(name, full, root, prefix)

            copy_file_or_dir(full, dst_full)
            os.chmod(dst_full, 0777)

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
