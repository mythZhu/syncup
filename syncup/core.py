#!/usr/bin/env python

import os
import sys

from syncup.dist import Distribution
from syncup.meta import DistributionMetadata
from syncup.debug import DEBUG


def get_metadata(**attrs):
    fpath = attrs.get('path')
    if fpath:
        return DistributionMetadata(fpath)

    name = attrs.get('name')
    version = attrs.get('version')

    if name and version:
        from syncup import metadata
        fsite = os.path.dirname(metadata.__file__)
        fname = '%s-%s.py' % (name, version)
        fpath = os.path.join(fsite, fname)
        if not os.path.exists(fpath):
            fpath = None
        return DistributionMetadata(fpath)
    else:
        return DistributionMetadata()


def get_distribution(**attrs):
    meta = attrs.get('metadata')
    if meta:
        del attrs['metadata']
    else:
        path = attrs.pop('metapath', None)
        name = attrs.pop('name', None)
        version = attrs.pop('version', None)
        meta = get_metadata(path=path, name=name, version=version)

    meta.do_update(attrs)

    if DEBUG:
        print >> sys.stdout, 'D: load metadata %s' % meta._path
        print >> sys.stdout, 'D: dump distribution metadata'
        print >> sys.stdout, meta

    return Distribution(meta)


def syncup(dist, target, **options):
    freeze_keys = (
        'root',
        'lib_paths',
        'data_paths',
        'script_paths'
        )
    others_keys = (
        'target',
        'nopyc',
        'lib_prefix',
        'data_prefix',
        'script_prefix'
        )

    freeze_opts = {}
    others_opts = {'target': target}

    for key, val in options.iteritems():
        if key in freeze_keys:
            freeze_opts[key] = options[key]
        elif key in others_keys:
            others_opts[key] = options[key]
        else:
            raise TypeError, \
                  'syncup() got an unexpected keyword argument %s' % key

    output = dist.freeze(**freeze_opts)

    if DEBUG:
        print >> sys.stdout, 'D: freeze %s distribution files' % len(output)
        for (name, full, root, prefix) in output:
            print >> sys.stdout, 'D: include %s' % full

    if target and target.lower().endswith('.zip'):
        dist.zip(**others_opts)
    else:
        dist.clone(**others_opts)

    if DEBUG:
        print >> sys.stdout, 'D: clone distribution to %s' % target

    return os.path.exists(target)
