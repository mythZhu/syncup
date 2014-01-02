#!/usr/bin/env python

import os
import tempfile

from syncup.cmd import Command
from syncup.util import change_root, copy_file_or_dir, remove_file_or_dir
from syncup.errors import CommandError


class clone(Command):

    def init_options(self):
        self.target_dir = None
        self.dist_files = None
        self.nopyc = False

    def main(self):
        if self.dist_files is None:
            cached = self.distribution.dist_cache.get('freeze')
            if cached is None:
                raise CommandError, 'please run freeze command before.'
            else:
                self.dist_files = cached

        if self.target_dir is None:
            self.target_dir = tempfile.mktemp()

        if os.path.exists(self.target_dir):
            remove_file_or_dir(self.target_dir)
        os.makedirs(self.target_dir)

        for f in filter(os.path.isfile, self.dist_files):
            if self.nopyc and f.endswith(('.pyc', '.pyo')):
                continue
            copy_file = change_root(self.target_dir, f)
            copy_file_or_dir(f, copy_file, force=True)

        return self.target_dir
