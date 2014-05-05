import logging

from zope.interface import implementer
from pyramid.security import has_permission
from pyramid.traversal import find_interface

from betahaus.viewcomponent.interfaces import IViewAction
from betahaus.viewcomponent.interfaces import IViewGroup
from betahaus.viewcomponent.compat import string_types

logger = logging.getLogger(__name__)


@implementer(IViewGroup)
class ViewGroup(object):
    """ Named utility for views. Behaves much like an ordered dict.
        See interfaces.py for documentation.
    """
    
    def __init__(self, name = None, perm_checker = None):
        self.name = name
        if perm_checker is None:
            perm_checker = has_permission
        self.perm_checker = perm_checker
        self._order = []
        self._data = {}
    
    def __call__(self, context, request, **kw):
        va_output = [x(context, request, **kw) for x in self.values()]
        return "".join([x for x in va_output if x])

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        assert isinstance(value, ViewAction)
        value.parent = self
        if value.priority is not None:
            index = len(self)
            for va in reversed(self.values()):
                if va.priority is not None and va.priority <= value.priority:
                    break
                index -= 1
            self.order.insert(index, key)
        else:
            self.order.append(key)
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]
        if key in self._order:
            self._order.remove(key)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, values):
        handle_keys = set(self.order)
        values = [unicode(x) for x in values]
        bad_keys = set()
        new_order = []
        while values:
            val = values.pop(0)
            if val in handle_keys:
                handle_keys.remove(val)
                new_order.append(val)
            else:
                bad_keys.add(val)
        if bad_keys:
            logger.warning("The following keys didn't exist: '%s'" % "', '".join(bad_keys))
        if handle_keys:
            logger.warning("The following keys were appended at the end since they existed: '%s'" % "', '".join(handle_keys))
            new_order.extend(handle_keys)
        self._order = new_order

    def get_context_vas(self, context, request): # pragma: no cover
        # backward compat, not needed
        return self.values()

    def add(self, view_action):
        self[view_action.name] = view_action

    def get(self, key, default=None):
        return self._data.get(key, default)

    def keys(self):
        return self.order

    def values(self):
        return [self[key] for key in self.order]

    def items(self):
        return [(name, self[name]) for name in self.order]

    def __repr__(self): # pragma : no cover
        klass = self.__class__
        classname = '%s.%s' % (klass.__module__, klass.__name__)
        return "<%s '%s'>" % (classname, self.name)


@implementer(IViewAction)
class ViewAction(object):

    def __init__(self, _callable, name, title = u"",
                 permission = None, interface = None, containment = None, priority=None, **kw):
        assert callable(_callable), "First argument must be a callable"
        assert isinstance(name, string_types), "Second argument name should be a string"
        self.callable = _callable
        self.name = name
        self.title = title
        self.permission = permission
        self.interface = interface
        self.containment = containment
        self.priority = priority
        self.kwargs = kw
        self.parent = None

    def __call__(self, context, request, **kw):
        if self.interface and not self.interface.providedBy(context):
            return
        if self.permission and not self.parent.perm_checker(self.permission, context, request):
            return
        if self.containment and not find_interface(context, self.containment):
            return
        return self.callable(context, request, self, **kw)

    def __repr__(self): # pragma : no cover
        klass = self.__class__
        classname = '%s.%s' % (klass.__module__, klass.__name__)
        return "<%s '%s'>" % (classname, self.name)
