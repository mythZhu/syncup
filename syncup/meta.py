#!/usr/bin/env python

from syncup.errors import MetadataError


class DistributionMetadata(object):

    _VALID_NAMES = (
        'name',
        'version',
        'packages',
        'py_modules',
        'scripts',
        'data_files',
    )

    def __init__(self, path=None):
        self.name = 'UNKNOWN'
        self.version = '0.0.0'
        self.packages = []
        self.py_modules = []
        self.scripts = []
        self.data_files = []

        if path is not None:
            self.do_import(path)

    def __repr__(self):
        lines = []
        for (key, val) in self.iteritems():
            if isinstance(val, list) or\
               isinstance(val, tuple):
                val = '\n  '.join(val)
            line = '[%s]\n  %s' % (key, val)
            lines.append(line)
        return '\n'.join(lines)

    def iteritems(self):
        for key in self._VALID_NAMES:
            yield (key, getattr(self, key))

    def do_update(self, attrs):
        for (key, val) in attrs.iteritems():
            if hasattr(self, key):
                setattr(self, key, val)
            else:
                raise MetadataError, \
                      'Invalid metadata attribute: %s' % key

    def do_import(self, path):
        try:
            global_ns = {}
            local_ns = {}
            execfile(path, global_ns, local_ns)
        except IOError:
            raise MetadataError, \
                  'No such file: %s' % path
        else:
            self.do_update(local_ns)
            self._path = path
