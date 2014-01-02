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
    output = dist.run_command('freeze', **options)

    if DEBUG:
        print >> sys.stdout, 'D: freeze %s distribution files' % len(output)
        for out in output:
            print >> sys.stdout, 'D: include %s' % out

    dist.run_command('clone', target_dir=target, nopyc=True)

    if DEBUG:
        print >> sys.stdout, 'D: clone distribution to %s' % target

    return os.path.isdir(target)
