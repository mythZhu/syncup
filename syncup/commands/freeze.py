#!/usr/bin/env python

from syncup.cmd import Command


class freeze(Command):

    def init_options(self):
        self.lib_paths = None
        self.data_paths = None
        self.script_paths = None
        self.root = '/'

    def main(self):
        lib = self.run_command(
                'freeze_lib',
                paths=self.lib_paths, root=self.root)
        dat = self.run_command(
                'freeze_data',
                paths=self.data_paths, root=self.root)
        bin = self.run_command(
                'freeze_script',
                 paths=self.script_paths, root=self.root)

        output = []
        output.extend(lib)
        output.extend(dat)
        output.extend(bin)

        return output
