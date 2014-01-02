#!/usr/bin/env python

class SyncupError(Exception):
    pass

class CommandError(SyncupError):
    pass

class DistributionError(SyncupError):
    pass

class MetadataError(SyncupError):
    pass
