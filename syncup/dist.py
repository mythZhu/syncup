#!/usr/bin/env python

import os
import sys
from imp import find_module, load_module

from syncup.meta import DistributionMetadata
from syncup.errors import DistributionError, CommandError


class Distribution(object):

    _VALID_NAMES = (
        'name',
        'version',
        'packages',
        'py_modules',
        'scripts',
        'data_files',
    )

    def __init__(self, meta=None):
        self.name = 'UNKNOWN'
        self.version = '0.0.0'
        self.packages = []
        self.py_modules = []
        self.scripts = []
        self.data_files = []

        if meta is None:
            meta = DistributionMetadata()
        if not isinstance(meta, DistributionMetadata):
            raise TypeError, \
                  'meta must be a DistributionMetadata instance'

        for (key, val) in meta.iteritems():
            if hasattr(self, key):
                setattr(self, key, val)
            else:
                raise DistributionError, \
                      'Invalid distribution attribute: %s' % key

        # 'dist_cache' is the dict of {command: output} that
        # have been created by an dist commands run so far.
        self.dist_cache = {}

    def get_command_obj(self, command):
        from syncup import commands
        try:
            site = commands.__path__
            name = command.lower()
            pymd = load_module(name, *find_module(name, site))
            cmd_cls = pymd.__dict__[name]
        except (ImportError, KeyError):
            raise CommandError, 'Invalid command name: %s' % command

        return cmd_cls(self)

    def run_command(self, command, **options):
        cmd_obj = self.get_command_obj(command)
        return cmd_obj.run(**options)
