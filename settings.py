try:
    from settings_dev import *
except ImportError:
    from settings_prod import *