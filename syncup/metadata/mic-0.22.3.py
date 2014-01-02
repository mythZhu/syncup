#!/usr/bin/env python

name = 'mic'

version = '0.22.3'

packages = [
    'mic',
    'mic/utils',
    'mic/imager',
    'mic/kickstart',
    'mic/kickstart/custom_commands',
    'mic/3rdparty/pykickstart',
    'mic/3rdparty/pykickstart/commands',
    'mic/3rdparty/pykickstart/handlers',
    'mic/3rdparty/pykickstart/urlgrabber',
    ]

scripts = [
    'mic',
    ]

data_files = [
    '/etc/mic',
    '/etc/bash_completion.d/mic.sh',
    '/etc/zsh_completion.d/_mic',
    'lib/mic/plugins/imager',
    'lib/mic/plugins/backend',
    'share/doc/mic-0.22.3',
    'share/man/man1/mic.1.gz'
    ]
