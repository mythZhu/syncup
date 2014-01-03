#!/usr/bin/env python

import os
import sys

from syncup.dist import Distribution
from syncup.meta import DistributionMetadata


__all__ = [
    'Distribution',
    'DistribuitonMetadata',
    'get_meta_from_path',
    'get_meta_from_name',
    'get_dist_from_meta',
    'get_dist_from_path',
    'get_dist_from_name',
    'freeze',
    'syncup',
    ]


def get_meta_from_path(path):
    return DistributionMetadata(path)


def get_meta_from_name(name, version):
    path = None

    if name and version:
        from syncup import metadata
        fsite = os.path.dirname(metadata.__file__)
        fname = '%s-%s.py' % (name, version)
        fpath = os.path.join(fsite, fname)
        if os.path.exists(fpath):
            path = fpath

    return get_meta_from_path(path)


def get_dist_from_meta(meta):
    if not isinstance(meta, DistributionMetadata):
        raise TypeError, 'meta is not instance of DistributionMetadata'

    return Distribution(meta)


def get_dist_from_path(path):
    meta = get_meta_from_path(path)
    return get_dist_from_meta(meta)


def get_dist_from_name(name, version):
    meta = get_meta_from_name(name, version)
    return get_dist_from_meta(meta)


def freeze(**options):
    dist = options.pop('dist', None)
    if dist is None:
        meta = options.pop('meta', None)
        path = options.pop('path', None)
        name = options.pop('name', None)
        version = options.pop('version', None)
        if meta:
            dist = get_dist_from_meta(meta)
        elif path:
            dist = get_dist_from_path(path)
        else:
            dist = get_dist_from_name(name, version)

    cmd = dist.freeze

    return cmd(**options)


def syncup(**options):
    dist = options.pop('dist', None)
    if dist is None:
        meta = options.pop('meta', None)
        path = options.pop('path', None)
        name = options.pop('name', None)
        version = options.pop('version', None)
        if meta:
            dist = get_dist_from_meta(meta)
        elif path:
            dist = get_dist_from_path(path)
        else:
            dist = get_dist_from_name(name, version)

    try:
        dist.dist_cache['freeze_lib']
        dist.dist_cache['freeze_data']
        dist.dist_cache['freeze_script']
    except KeyError:
        dist.freeze()

    target = options['target']
    if target.lower().endswith('.zip'):
        cmd= dist.zip
    else:
        cmd = dist.clone

    return cmd(**options)
