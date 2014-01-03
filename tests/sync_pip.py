#!/usr/bin/env python

from syncup.core import syncup


if __name__ == '__main__':
    output = syncup(name='pip', version='1.3.1', target='/tmp/pip')
    print output
