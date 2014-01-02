#!/usr/bin/env python

from syncup.core import get_distribution, syncup


if __name__ == '__main__':
    target = '/tmp/mic'
    name = 'mic'
    version = '0.22.3'

    dist = get_distribution(name=name, version=version)
    stat = syncup(dist, target)
