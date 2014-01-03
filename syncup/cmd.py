#!/usr/bin/env python

import sys

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

    def __getattr__(self, name):
        try:
            return getattr(self.distribution, name)
        except:
            raise AttributeError, name

    def parse_options(self, options):
        for (key, val) in options.iteritems():
            if hasattr(self, key):
                setattr(self, key, val)
            else:
                raise CommandError('Unknown command option: %s' % key)

    def dump_options(self, indent=''):
        if not hasattr(self, 'user_options'):
            return

        header = 'Command options for %s:' % self.__class__.__name__
        indent = indent + '  '

        lines = [header]
        for key, val in self.user_options.iteritems():
            lines.append(indent + '%s = %s' % (key, val))

        print >> sys.stdout, '\n'.join(lines)

    def dump_output(self, indent=''):
        if not hasattr(self, 'output'):
            return

        header = 'Command output for %s:' % self.__class__.__name__
        indent = indent + '  '

        lines = [header]
        if isinstance(self.output, (list, tuple)):
            for item in self.output:
                lines.append(indent + repr(item))
        else:
            lines.append(self.output)

        print >> sys.stdout, '\n'.join(lines)

    def run(self, **options):
        self.user_options = options
        self.parse_options(options)

        if DEBUG:
            self.dump_options(indent='  ')

        self.output = self.main()
        self.distribution.dist_cache[self.__class__.__name__] = self.output

        if DEBUG:
            self.dump_output(indent='  ')

        return self.output

    # Subclasses must define:
    #   init_options()
    #     provide default values for all options
    #   main()
    #     execute the command

    def init_options(self):
        raise RuntimeError, \
              'abstract method -- subclass %s must override' % self.__class__

    def main(self):
        raise RuntimeError, \
              'abstract method -- subclass %s must override' % self.__class__
