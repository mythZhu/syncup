syncup
======

what is syncup
--------------

`syncup` is a python package which provides awesome functions to collect
and manage all files belong to a python distribution

how to use
----------

A python distribution usually consists of packages, modules, scripts and
addation data. If you want `syncup` to collect a python distribuiton,
you MUST supply a metadata file for it.

The following is the metadata file for `pip-1.3.1`:

```
dist_name = 'pip'
dist_version = '1.3.1'
packages = ['pip']
scripts = ['pip', 'pip-python', 'python-pip']
data = ['share/doc/python-pip-1.3.1']
```

look, it is just a common python file.

NOTE: If you tired to supply the path of metadata file to `syncup`
explicitly, you just put it under the path `syncup/metata` and name it
`[name]-[version].py`.


Then, you can call `syncup` functions to manage a python distribution:

```
from syncup.core import *

# if there is a metadata file under 'syncup/metadata'
# you can get a dist object via its name and version
dist = get_dist_from_name(name, version)


# if you want to specify a metadata file for a distribution
# you can do it like this
dist = get_dist_from_path(path)


# if you have created a metadata object by yourself
# you can also get a dist object from it directly
dist = get_dist_from_meta(meta)


# with dist object
# you can dump all dist files belong to it
freeze(dist=dist)


# without dist object
# you can supply a metadata object or a metadata file
# or dist name & version
freeze(meta=meta)
freeze(path=path)
freeze(name=name, version=version)


# more, you can supply search paths for freeze()
# it will search dist files under them
freeze(
    dist=dist,
    lib_paths=your_lib_paths,
    data_paths=your_data_paths,
    script_paths=your_script_paths
)


# syncup() is a more powerful function
# you can copy a python distribuiton into a directory
syncup(dist=dist, target=target)
syncup(meta=meta, target=target)
syncup(path=path, target=target)
syncup(name=name, version=version, target)


# more, you can specify paths prefix for syncup()
# it will store dist files with them
syncup(
    dist=dist,
    target=target,
    lib_prefix=your_lib_prefix,
    data_prefix=your_data_prefix,
    script_prefix=your_script_prefix,
)
```

license
-------


author
------

Written by Myth
