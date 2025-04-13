module_loaded = True

#   The documentation for the importlib.resources API is found at:
#     https://importlib-resources.readthedocs.io/en/latest/using.html
#     https://docs.python.org/3/library/importlib.resources.html
#     https://docs.python.org/3/library/importlib.resources.abc.html#importlib.resources.abc.Traversable
#
#   An "anchor" is a start point for a tree of resources, either a
#   module object or a module name as a string (`Union[str, ModuleType]`).
#   • If no anchor is supplied, the current module is used. (Since 3.12.)
#   • If the anchor is an (import) package, that package is used as
#     the root of the resource tree.
#     (Since 3.9. Pre-3.12 the param name was `package`.)
#   • If the anchor is a non-package module (e.g., `foo` read from `foo.py`)
#     the "directory" containing the package is the root of the resource
#     tree (i.e., the resources are adjacent to the module, not below it).
#     (Since 3.12.)
#
#   The "functional" API is a simpler set of higher level functions
#   over the core API.
#
#   Functions that do not need to extract to filesystem. These were
#   introduced in 3.7, deprecated in 3.11 and un-deprecated in 3.12.
#   ● is_resource(anchor, *path_components)
#     - Directories are not considered to be resources.
#   ● read_binary(anchor, *path_components)
#     - Returns `bytes`.
#   ● open_binary(anchor, *path_components)
#     - Return `BinaryIO`.
#   ● read_text(anchor, *path_components, encoding='utf-8', errors='strict')
#     - Returns `str`.
#   ● open_text(anchor, *path_components, encoding='utf-8', errors='strict')
#     - Returns `TextIO`.
#     - Always give `encoding` explicitly, or third argument will be
#       `encoding`. (Until Python 3.15.)
#
#   Functions that will extract to filesystem:
#   ● path(anchor, *path_components)
#     - Context manager; `with` gives a `pathlib.Path`.
#
#   Deprecated:
#   ● contents(anchor, *path_components)
#     - Deprecated since 3.11; use iterdir().
#
#   Core API:
#   ● files(anchor)     # Since 3.9.
#     - Returns a `Traversable` representing the resource container
#       ("directory") containing resources ("files') and further
#       containers ("subdirs").
#   ● as_file(traversable)
#

#   Instead of importlib.resources, which has lots of annoying variations
#   from 3.7 through 3.12, we use the backported version from PyPI.
from importlib_resources  import files as resfiles

def contents_textfile():
    ''' Read the ``textfile`` resource.
        1. The no-argument version of `files()` is not available before
           Python 3.12; we must install the PyPI ``importlib-resources``\
           package to get it in Python ≤ 3.11.
        2. The use of `importlib.resources.open_text()` etc. has been
           on-again/off-again in terms of recommendataions; it's best just
           to use `files()` since it's about as simple anyway.
    '''
    return resfiles().joinpath('textfile').read_text()
