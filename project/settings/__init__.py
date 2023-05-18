import os

debug = os.environ.get("DEBUG", True)
if debug:
    from .dev import *
else:
    from .prod import *