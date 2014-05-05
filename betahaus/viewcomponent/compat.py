import sys

PY3 = sys.version_info[0] == 3

if PY3: # pragma: no cover
    string_types = str,
    text_type = str
else: # pragma: no cover
    string_types = basestring,
    text_type = unicode
