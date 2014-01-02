#!/usr/bin/env python

import os
import zipfile
import tempfile

from syncup.cmd import Command
from syncup.util import remove_file_or_dir
from syncup.errors import CommandError


class zip(Command):

    def init_options(self):
        self.target = None
        self.dist_files = None
        self.nopyc = False

    def main(self):
        if self.dist_files is None:
            cached = self.distribution.dist_cache.get('freeze')
            if cached is None:
                raise CommandError, 'please run freeze command before.'
            else:
                self.dist_files = cached

        if self.target is None:
            self.target = tempfile.mktemp()

        if os.path.exists(self.target):
            remove_file_or_dir(self.target)

        target_dir = os.path.dirname(self.target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        zip = zipfile.ZipFile(self.target, 'w')
        for f in filter(os.path.isfile, self.dist_files):
            if self.nopyc and f.endswith(('.pyc', '.pyo')):
                continue
            zip.write(f)
        zip.close()

        return self.target
