syncup
======

what is syncup
--------------

`syncup` provides functions to collect all files belong to a python
distribution and manage them.

how to use
----------

A python distribution consists of packages, modules, scripts and data.
If you want `syncup` to collect all distribuiton files, you MUST supply
a metadata file for the specified distribution. The following is the
metadata file for `pip-1.3.1`:

```
dist_name = 'pip'
dist_version = '1.3.1'
packages = ['pip']
scripts = ['pip', 'pip-python', 'python-pip']
data = ['share/doc/python-pip-1.3.1']
```

NOTE: If you don't want to always supply the path of metadata file to
`syncup` explicitly, you can put it under the path `syncup/metata` and
name it `[name]-[version].py`.

After this, you can call `syncup` function to collect a python distribution
into a directory or zip file like the following examples:

```
from syncup.core import get_distribution, syncup

# if there is a metadata file under 'syncup/metadata'
dist = get_distribution(name=name, version=version)
syncup(dist, target_dir)

# otherwise
dist = get_distribution(metapath=meta_file_path)
syncup(dist, target_dir)

# if you want to collect the distribution into a zip file
# you just make sure that 'target_zip' ends with '.zip' 
dist = get_distribution(name=name, version=version)
syncup(dist, target_zip)
```

license
-------


author
------

Written by Myth
