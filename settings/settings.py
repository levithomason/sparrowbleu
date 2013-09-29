try:
    from dev import *
except ImportError:
    from production import *