import venusian

from zope.interface import implements
from zope.interface.interfaces import ComponentLookupError
from pyramid.security import has_permission
from pyramid.traversal import find_interface

from betahaus.viewcomponent.interfaces import IViewGroup


class ViewGroup(dict):
    """ Named utility for views. Behaves like a dict with some extra funkyness."""
    implements(IViewGroup)
    
    def __init__(self, perm_checker = None):
        if perm_checker is None:
            perm_checker = has_permission
        self.perm_checker = perm_checker
    
    def __call__(self, context, request):
        for va in self.get_context_vas(context, request):
            yield va(context, request)

    def get_context_vas(self, context, request):
        for va in self.values():
            if va.interface and not va.interface.providedBy(context):
                continue
            if va.permission and not self.perm_checker(va.permission, context, request):
                continue
            if va.containment and not find_interface(context, va.containment):
                continue
            yield va

    def add(self, view_action):
        self[view_action.name] = view_action

    def __setitem__(self, key, value):
        assert isinstance(value, ViewAction)
        super(ViewGroup, self).__setitem__(key, value)


class ViewAction(object):

    def __init__(self, _callable, name, title = u"", description = u"",
                 permission = None, interface = None, containment = None):
        assert callable(_callable)
        assert isinstance(name, basestring)
        self.callable = _callable
        self.name = name
        self.title = title
        self.description = description
        self.permission = permission
        self.interface = interface
        self.containment = containment

    def __call__(self, context, request, **kw):
        return self.callable(context, request, self, **kw)

    def __repr__(self): # pragma : no cover
        klass = self.__class__
        classname = '%s.%s' % (klass.__module__, klass.__name__)
        return "<%s '%s'>" % (classname, self.name)


class view_action(object):
    """ Decorator for menu actions. This sets up a ViewAction object from a decorated callable """
    venusian = venusian
    
    def __init__(self, group_name, action_name,
                 **kwargs):
        self.group_name = group_name
        self.action_name = action_name
        self.kwargs = kwargs

    def register(self, scanner, name, wrapped):
        view_group = scanner.config.registry.queryUtility(IViewGroup, name = self.group_name)
        if view_group is None:
            view_group = ViewGroup()
            scanner.config.registry.registerUtility(view_group, IViewGroup, name = self.group_name)
        va =  ViewAction(wrapped, self.action_name, **self.kwargs)
        view_group.add(va)

    def __call__(self, wrapped):
        self.venusian.attach(wrapped, self.register, category='betahaus.viewcomponent')
        return wrapped


def render_view_group(context, request, name):
    util = request.registry.getUtility(IViewGroup, name = name)
    return "".join(util(context, request))
