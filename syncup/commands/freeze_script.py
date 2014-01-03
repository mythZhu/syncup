#!/usr/bin/env python

import os
import sys
import site

from syncup.cmd import Command
from syncup.util import change_root, get_os_paths, get_home_path
from syncup.errors import CommandError


class freeze_script(Command):

    def init_options(self):
        self.paths = None
        self.root = '/'

    def bin_paths(self):
        if self.paths:
            select_paths = self.paths
        else:
            select_paths = []
            # TODO: more availabe search paths
            select_paths.extend(get_os_paths())
            select_paths.append('/bin')
            select_paths.append('/sbin')
            select_paths.append('/usr/bin')
            select_paths.append('/usr/sbin')
            select_paths.append('/usr/local/bin')
            select_paths.append('/usr/local/sbin')
            select_paths.append(os.path.join(sys.prefix, 'bin'))
            select_paths.append(os.path.join(sys.prefix, 'sbin'))
            select_paths.append(os.path.join(sys.prefix, 'local/bin'))
            select_paths.append(os.path.join(sys.prefix, 'local/sbin'))
            select_paths.append(os.path.join(get_home_path(), 'bin'))
            select_paths.append(os.path.join(site.USER_BASE, 'bin'))
        return select_paths

    def find_script(self, script):
        for prefix in self.bin_paths():
            path = change_root(self.root, prefix)
            full = os.path.join(path, script)
            if os.path.isfile(full):
                return (script, full, self.root, prefix)
        else:
            raise CommandError, 'No script with the name %s found' % script

    def main(self):
        scripts = []
        for script in self.distribution.scripts:
            scripts.append(self.find_script(script))
        return scripts
