# Choose the right settings, development is excluded from the repo so its only loaded locally

try:
    from development import *
except ImportError:
    from production import *
