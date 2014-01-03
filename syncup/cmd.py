#!/usr/bin/env python

from syncup.dist import Distribution
from syncup.errors import CommandError
from syncup.debug import DEBUG


class Command(object):

    def __init__(self, dist):
        if not isinstance(dist, Distribution):
            raise TypeError, 'dist must be a Distribution instance'
        if self.__class__ is Command:
            raise RuntimeError, 'Command is an abstract class'

        self.init_options()
        self.distribution = dist

    def init_options(self):
        raise RuntimeError, \
              'abstract method -- subclass %s must override' % self.__class__

    def parse_options(self, options):
        for (key, val) in options.iteritems():
            if hasattr(self, key):
                setattr(self, key, val)
            else:
                raise CommandError('Unknown command option: %s' % key)

    def main(self):
        raise RuntimeError, \
              'abstract method -- subclass %s must override' % self.__class__

    def run_command(self, command, **options):
        return self.distribution.run_command(command, **options)

    def run(self, **options):
        self.parse_options(options)
        output = self.main()
        self.distribution.dist_cache[self.__class__.__name__] = output
        return output
