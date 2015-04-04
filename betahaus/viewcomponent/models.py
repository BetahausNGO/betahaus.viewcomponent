import logging

from zope.interface import implementer
from pyramid.security import has_permission
from pyramid.traversal import find_interface

from betahaus.viewcomponent.interfaces import IViewAction
from betahaus.viewcomponent.interfaces import IViewGroup
from betahaus.viewcomponent.compat import string_types
from pyramid.threadlocal import get_current_registry

logger = logging.getLogger(__name__)

_marker = object()
_empty_vals = ('', None)


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
    
    def __call__(self, context, request,
                 as_type = None, spacer = "", empty_val = _marker, **kw):
        if as_type is None:
            return spacer.join([x for x in self.as_generator(context, request, empty_val = empty_val, **kw)])
        try:
            type_method = getattr(self, 'as_%s' % as_type)
        except AttributeError:
            raise ValueError("as_type must be a valid output type or None, was: %r" % as_type)
        return type_method(context, request, empty_val = empty_val, **kw)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        assert isinstance(value, ViewAction)
        value.parent = self
        if value.priority is not None:
            if key in self.order:
                self.order.remove(key)
            index = len(self)
            for va in reversed(self.values()):
                if va.priority is not None and va.priority <= value.priority:
                    break
                index -= 1
            self.order.insert(index, key)
        else:
            if key not in self.order:
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

    def as_generator(self, context, request, empty_val = _marker, **kw):
        for x in self.values():
            res = x(context, request, **kw)
            if res in _empty_vals:
                if empty_val != _marker:
                    yield empty_val
            else:
                yield res

    def as_dict(self, context, request, empty_val = _marker, **kw):
        va_output = {}
        for (k, v) in self.items():
            res = v(context, request, **kw)
            if res in _empty_vals:
                if empty_val != _marker:
                    va_output[k] = empty_val
            else:
                va_output[k] = res
        return va_output

    def as_list(self, context, request, empty_val = _marker, **kw):
        return list(self.as_generator(context, request, empty_val = empty_val, **kw))

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


def add_view_action(_callable, group_name, name, priority = None, registry = None, **kwargs):
    """ Create a new view action and possibly add a view group if it doesn't exist.
        Use the decorator or the directive instead of this method directly.
    """
    if registry is None: # pragma : no cover
        registry = get_current_registry()
    view_group = registry.queryUtility(IViewGroup, name = group_name)
    if view_group is None:
        view_group = ViewGroup(group_name)
        registry.registerUtility(view_group, IViewGroup, name = group_name)
    va = ViewAction(_callable, name, priority = priority, **kwargs)
    view_group.add(va)
    return va
