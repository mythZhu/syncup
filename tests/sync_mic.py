#!/usr/bin/env python

from syncup.core import syncup


if __name__ == '__main__':
    output = syncup(name='mic', version='0.22.3', target='/tmp/mic')
    print output
