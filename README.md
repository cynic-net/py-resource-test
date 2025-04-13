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



<!-------------------------------------------------------------------->
[importlib-resources]: https://pypi.org/project/importlib-resources/
