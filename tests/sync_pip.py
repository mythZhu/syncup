#!/usr/bin/env python

from syncup.core import get_distribution, syncup


if __name__ == '__main__':
    target = '/tmp/pip'
    name = 'pip'
    version = '1.3.1'

    dist = get_distribution(name=name, version=version)
    stat = syncup(dist, target)
