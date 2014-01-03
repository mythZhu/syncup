#!/usr/bin/env python

import os
import sys
import glob
import shutil

from distutils.util import change_root


def get_os_paths():
    os_paths = []
    if os.environ.has_key('PATH'):
        os_paths.extend(os.environ['PATH'].split(':'))
    return os_paths


def get_home_path(user=None):
    if user:
        return os.path.expanduser('~' + user)
    else:
        return os.path.expanduser('~')


def remove_file_or_dir(file_or_dir):
    """ Remove a file node whatever its type.
    """
    if not os.path.exists(file_or_dir):
        return True

    if os.path.isdir(file_or_dir):
        shutil.rmtree(file_or_dir)
    else:
        os.unlink(file_or_dir)

    return os.path.exists(file_or_dir)


def copy_file_or_dir(file_or_dir, dest_path, force=False,
                     symlinks=False,ignores=()):
    """ Copy a file node whatever its type.
    """
    if os.path.exists(dest_path):
        if force:
            remove_file_or_dir(dest_path)
        else:
            return False

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    if os.path.isdir(file_or_dir):
        ignores = shutil.ignore_patterns(*ignores)
        shutil.copytree(file_or_dir, dest_path, symlinks, ignores)

    else:
        if True not in map(file_or_dir.lower().endswith, ignores):
            shutil.copyfile(file_or_dir, dest_path)

    return os.path.exists(dest_path)


def walk_tree(top):
    nodes = [top]
    for dirpath, dirnames, filenames in os.walk(top):
        for dirname in dirnames:
            nodes.append(os.path.join(dirpath, dirname))
        for filename in filenames:
            nodes.append(os.path.join(dirpath, filename))

    return nodes


def real_prefix(prefix):
    if hasattr(sys, 'real_prefix') and prefix.find(sys.prefix) == 0:
        prefix = prefix[len(sys.prefix):]
        prefix = os.path.join(sys.real_prefix, prefix)
    return prefix
