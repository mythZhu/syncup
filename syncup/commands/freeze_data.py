#!/usr/bin/env python

import os
import sys
import site

from syncup.cmd import Command
from syncup.util import walk_tree, change_root, get_home_path
from syncup.errors import CommandError


class freeze_data(Command):

    def init_options(self):
        self.paths = None
        self.root = None

    def dat_paths(self):
        if self.paths:
            select_paths = self.paths
        else:
            select_paths = []
            # TODO: more availabe search paths
            select_paths.append(sys.prefix)
            select_paths.append(os.path.join(sys.prefix, 'local'))
            select_paths.append(get_home_path())
            select_paths.append(site.USER_BASE)

        if self.root:
            select_paths = [ change_root(self.root, p) for p in select_paths ]

        return select_paths

    def find_data(self, data):
        for path in self.dat_paths():
            full = os.path.join(path, data)
            if os.path.exists(full):
                return data, full
        else:
            raise CommandError, 'No data with the name %s found' % data

    def main(self):
        data_files = []
        for data_file in self.distribution.data_files:
            fname, fpath = self.find_data(data_file)
            data_files.append(fpath)

        output = []
        for data in data_files:
            if data in output:
                continue
            output.extend(walk_tree(data))
        return output
