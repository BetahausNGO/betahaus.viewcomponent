from betahaus.viewcomponent.decorators import view_action
from betahaus.viewcomponent.interfaces import IViewGroup
from betahaus.viewcomponent.models import add_view_action


def render_view_group(context, request, group, **kw):
    """ Turn everything in a view action into a string or pick another format by
        specifying as_type.
        
        See IViewGroup for full options.
    """
    util = request.registry.getUtility(IViewGroup, name = group)
    return util(context, request, **kw)

def render_view_action(context, request, group, name, **kw):
    """ Return the result of a single view action."""
    util = request.registry.getUtility(IViewGroup, name = group)
    return util[name](context, request, **kw)

def _view_action_directive(config, _callable, group_name, name,
                           priority = None, registry = None,
                           **kwargs):
    """ Use via config.add_view_action when you've included betahaus.viewcomponent. """
    return add_view_action(_callable, group_name, name,
                           priority = priority, registry = config.registry,
                           **kwargs)

def includeme(config):
    """ Include this if you wish to add view actions using directive instead, like:
    
        config.add_view_action(group_name, view_action_name, callable, <etc...>)
    """
    config.add_directive('add_view_action', _view_action_directive)
