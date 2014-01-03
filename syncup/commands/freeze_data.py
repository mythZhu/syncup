#!/usr/bin/env python

import os
import sys
import site

from syncup.cmd import Command
from syncup.util import change_root, get_home_path
from syncup.errors import CommandError


class freeze_data(Command):

    def init_options(self):
        self.paths = None
        self.root = '/'

    def dat_paths(self):
        if self.paths:
            select_paths = self.paths
        else:
            select_paths = []
            # TODO: more availabe search paths
            select_paths.append('/')
            select_paths.append('/usr')
            select_paths.append('/usr/local')
            select_paths.append(sys.prefix)
            select_paths.append(os.path.join(sys.prefix, 'local'))
            select_paths.append(get_home_path())
            select_paths.append(site.USER_BASE)
        return select_paths

    def find_data(self, data):
        for prefix in self.dat_paths():
            path = change_root(self.root, prefix)
            full = os.path.join(path, data)
            if os.path.exists(full):
                return (data, full, self.root, prefix)
        else:
            raise CommandError, 'No data with the name %s found' % data

    def main(self):
        data_files = []
        for data_file in self.distribution.data_files:
            data_files.append(self.find_data(data_file))
        return data_files
