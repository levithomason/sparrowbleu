import re


def _human_key(key):
    '''
    Sorts a list in natural sort fashion
    http://stackoverflow.com/questions/5295087/how-to-sort-alphanumeric-list-of-django-model-objects
    http://stackoverflow.com/questions/5254021/python-human-sort-of-numbers-with-alpha-numeric-but-in-pyqt-and-a-lt-oper/5254534#5254534
    '''
    parts = re.split('(\d*\.\d+|\d+)', key)
    return tuple((e.swapcase() if i % 2 == 0 else float(e)) for i, e in enumerate(parts))
