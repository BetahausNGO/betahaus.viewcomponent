from betahaus.viewcomponent.decorators import view_action
from betahaus.viewcomponent.interfaces import IViewGroup


def render_view_group(context, request, group, **kw):
    """ Render everything in a view group. """
    util = request.registry.getUtility(IViewGroup, name = group)
    return util(context, request, **kw)

def render_view_action(context, request, group, name, **kw):
    """ Render a single view action. """
    util = request.registry.getUtility(IViewGroup, name = group)
    return util[name](context, request, **kw)
