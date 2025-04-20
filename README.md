py-resource-test: Test use of importlib.resources
=================================================

This is just a small bit of research to figure out how to best use the
`importlib.resources` system and provide example code that has been
confirmed (though tests) to work, including with resources that are
not present as files in the filesystem (i.e., in a ZIP file library).

We're actually testing the backport [importlib-resources] from PyPI
(imported as `importlib_resources` instead of `importlib.resources`)
because using this gives us the same API everywhere, rather than the mess
of various APIs and deprecations we've seen in Pythons 3.7 through
3.12, when the API finally settled down.

We could also add tests showing how to use `importlib.resources` in ways
that will work across various versions of Python, but this doesn't seem
worthwhile as it's fairly difficult. (E.g., APIs that are good in Pythons
3.7–3.10 and ≥ 3.12 are deprecated in 3.11, so one would want to suppress
the warning messages about those there, or have some flag that uses
different APIs depending on the version of Python.)

### Files and Directories

Run `./Test` to run the tests; the `-c` option will do a clean build
(rebuilding the virtualenv, etc.).

`pylib` contains the sample library code and the resources; `client`
contains tests that import and call the library.


importlib.resources API
-----------------------

The documentation for the importlib.resources API is found at:
- [Using importlib_resources][i_r-using]: General usage overview.
- [`importlib.resources` – Package resource reading, opening and
  access][i.r-package]: API details for current version of Python. (Use the
  version number drop-down menu at the upper left of the page to see APIs
  for other versions of Python.)
- [`importlib.resources.abc.Traversable`][i.r.abc.T]: API of the
  `Traversable` object (a type of [`pathlib.Path`]) returned by
  `importlib_resources.files()`.

Most functions take an _anchor_ (type `importlib_resources.Anchor`), a
start point for a tree of resources, which may be either a module object or
a module name as a string (`Union[str, ModuleType]`).
* If no anchor is supplied, the current module is used. (Since 3.12.)
* If the anchor is an (import) package, that package is used as the root of
  the resource tree. (Since 3.9. Pre-3.12 the param name was `package`.)
* If the anchor is a non-package module (e.g., `foo` read from `foo.py`)
  the "directory" containing the package is the root of the resource tree
  (i.e., the resources are adjacent to the module, not below it). (Since
  3.12.)

### Core API

The core API became available in Python 3.9, but is usable in any version
of Python ≥ 3.7 with the `importlib_resources` package.

The primary core API function is `importlib_resources.files(anchor: Anchor
| None = None)`. This is the only function where (as of Python 3.12 or in
the compatibility `importlib_resources` package) the anchor is optional,
defaulting to the current module. On the `Traversable` return value you may:
- Navigate the resource tree using [`Path.joinpath()`].
- Iterate directories using [`Path.iterdir()`], [`Path.glob()`],
  [`Path.rglob()`], and [`Path.walk()`].
- Open files using [`Path.open()`].
- Read file contents using [`Path.read_text()`] or [`Path.read_bytes()`].

(Forward slashes in path components given to these functions work
as directory seperators on all systems, including Windows.)

You may not, however, assume that the return value refers to a path in the
file system. If the package was loaded from a ZIP file, for example, it
will be a reference to the ZIP file and path within it. When you need a
reference to a directory or file in the filesystem, use [`as_file()`] to
temporarily generate one (if necessary) from a `files()` return value. Any
temporary file or directory will be cleaned up when you exit the `with`
context.

    t = importlib_resources.files()
    with importlib_resources.as_file(t) as p:
        ...   # operations on `Path` object `p` here

### Functional API

The "functional" API is just a bit of syntatic sugar over the core API
above. It suffers from two issues: it _always_ requires an `Anchor`
argument (you cannot use `None`) and it's been on-and-off deprecated over
time. However, these do work in older versions of Python if you're not
using `importlib_resources`: they were introduced in 3.7; the Core API
above not until 3.9. Note that these were deprecated in Python 3.11, and
undeprecated in Python 3.12.

To have these functions use resources relative to the current module, you
cannot pass `None` (as you can with `importlib_resources.files()`), so you
need to pass (generally) `__name__` to do that.

The following functions do not need to extract anything to the filesystem:

- `is_resource(anchor, *path_components)`. Note that directories are not
  considered to be resources.
- `read_binary(anchor, *path_components)`. Returns `bytes`.
- `open_binary(anchor, *path_components)`. Returns `BinaryIO`.
- `read_text(anchor, *path_components, encoding='utf-8', errors='strict')`.
  Returns `str`.
- `open_text(anchor, *path_components, encoding='utf-8', errors='strict')`
  Returns `TextIO`. Always give `encoding` parameter name explicitly, or
  third argument will be `encoding`. (Until Python 3.15.)
- `path(anchor, *path_components)`. Context manager returning a
  `pathlib.Path`. May extract some dirs/files to the filesystem, cleaning
  them up after the context manager exits.
- `contents(anchor, *path_components)`. Still deprecated since 3.11; use
  `iterdir()`.



<!-------------------------------------------------------------------->
[`as_file()`]: https://docs.python.org/3/library/importlib.resources.html#importlib.resources.as_file
[i.r-package]: https://docs.python.org/3/library/importlib.resources.html
[i.r.abc.T]: https://docs.python.org/3/library/importlib.resources.abc.html#importlib.resources.abc.Traversable
[i_r-using]: https://importlib-resources.readthedocs.io/en/latest/using.html
[importlib-resources]: https://pypi.org/project/importlib-resources/

[`Path.glob()`]: https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
[`Path.iterdir()`]: https://docs.python.org/3/library/pathlib.html#pathlib.Path.iterdir
[`Path.joinpath()`]: https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.joinpath
[`Path.open()`]: https://docs.python.org/3/library/pathlib.html#pathlib.Path.open
[`Path.read_bytes()`]: https://docs.python.org/3/library/pathlib.html#pathlib.Path.read_bytes
[`Path.read_text()`]: https://docs.python.org/3/library/pathlib.html#pathlib.Path.read_text
[`Path.rglob()`]: https://docs.python.org/3/library/pathlib.html#pathlib.Path.rglob
[`Path.walk()`]: https://docs.python.org/3/library/pathlib.html#pathlib.Path.walk
[`pathlib.path`]: https://docs.python.org/3/library/pathlib.html#pathlib.Path
