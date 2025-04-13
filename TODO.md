To-do
=====

- Test this in earlier versions of Python than 3.11.
  (Should be no issues because we're using backported module.)
- Test under Windows.
- Use native Python ZIP support instead of external `zip` program.
- Test that merge of resource trees from two separate namespace
  modules (e.g., `pylib/foo/` and `otherlib/foo/`, where both `pylib/`
  and `otherlib/` are in $PYTHONPATH) works.
