module_loaded = True

#   Instead of importlib.resources, which has lots of annoying variations
#   from 3.7 through 3.12, we use the backported version from PyPI.
from    importlib_resources  import files as resfiles
import  importlib_resources as resources

def read_textfile_core():
    ''' Use the core API to read the ``textfile`` resource.
        1. The no-argument version of `files()` is not available before
           Python 3.12; we must install the PyPI ``importlib-resources``\
           package to get it in Python ≤ 3.11.
        2. The use of `importlib.resources.open_text()` etc. has been
           on-again/off-again in terms of recommendataions; it's best just
           to use `files()` since it's about as simple anyway.
    '''
    return resfiles().joinpath('textfile').read_text()

def read_textfile_sugar_modreq():
    ''' Demo that old API can't take `None`, an `Anchor` is required. '''
    return resources.read_text(None, 'textfile')

def read_textfile_sugar_selfmodule():
    return resources.read_text(__name__, 'textfile')
