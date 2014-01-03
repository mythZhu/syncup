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

        self._path = 'DEFAULT'
        if path is not None:
            self.do_import(path)

    def __repr__(self):
        header = 'Distribution meta-data:'
        indent = '  '

        lines = []
        lines.append(header)
        lines.append(indent + '[metapath]')
        lines.append(indent*2 + self._path)

        for (key, val) in self.iteritems():
            lines.append(indent + '[%s]' % key)
            if isinstance(val, (list, tuple)):
                val = '\n'.join([ indent*2 + e for e in val ])
            else:
                val = indent*2 + val
            lines.append(val)

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
