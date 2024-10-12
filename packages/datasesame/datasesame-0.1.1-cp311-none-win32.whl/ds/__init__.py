import os
from .data import view

if not os.getenv('SKIP_IMPORT_DS'):
    from .ds import *
    __doc__ = ds.__doc__
    if hasattr(ds, "__all__"):
        __all__ = ds.__all__
