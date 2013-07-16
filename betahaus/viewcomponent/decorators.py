import venusian

from betahaus.viewcomponent.interfaces import IViewGroup
from betahaus.viewcomponent.models import ViewAction
from betahaus.viewcomponent.models import ViewGroup


class view_action(object):
    """Decorator for view actions. This sets up a ViewAction object
    from a decorated callable.
    
    group_name  -- the name of the group the decorated action is
                   supposed to be rendered with
    action_name -- cosmetic name of the decorated action
    priority    -- priority with which the decorated action is rendered
                   within the group
    """

    def __init__(
          self
        , group_name
        , action_name
        , priority=None
        , **kwargs):

        self.group_name = group_name
        self.action_name = action_name
        self.priority = priority
        self.kwargs = kwargs

    def register(self, scanner, name, wrapped):
        view_group = scanner.config.registry.queryUtility(IViewGroup, name = self.group_name)
        if view_group is None:
            view_group = ViewGroup(self.group_name)
            scanner.config.registry.registerUtility(view_group, IViewGroup, name = self.group_name)
        va =  ViewAction(wrapped, self.action_name, priority=self.priority, **self.kwargs)
        view_group.add(va)

    def __call__(self, wrapped):
        venusian.attach(wrapped, self.register, category='betahaus.viewcomponent')
        return wrapped
