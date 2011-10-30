from pyramid_debugtoolbar.panels import DebugPanel

from betahaus.viewcomponent.interfaces import IViewGroup


VA_ATTRS = ('title',
            'permission',
            'interface',
            'containment',)


class ViewGroupDebugPanel(DebugPanel):

    name = 'ViewGroup'
    has_content = True

    def __init__(self, request):
        self.request = request
        self.utils = tuple(self.request.registry.getUtilitiesFor(IViewGroup))

    def nav_title(self):
        return u"View Groups"

    title = nav_title

    def nav_subtitle(self):
        num = len(self.utils)
        return '%d %s' % (num, self.pluralize("view group", "view groups", num))

    def url(self):
        return ''

    def content(self):
        vars = dict(
            utils = self.utils,
            va_attrs = VA_ATTRS,
            callable_repr = self.callable_repr,
        )
        return self.render(
            'betahaus.viewcomponent:debug_panel.pt',
            vars,
            request=self.request)

    def callable_repr(self, _callable):
        return '%s.<b>%s</b>' % (_callable.__module__, _callable.__name__)


def includeme(config):
    """ Activate the debug toolbar; usually called via
        ``config.include('betahaus.viewcomponent.debug_panel')`` 
        instead of being invoked directly.
    """
    try:
        panels = config.registry.settings['debugtoolbar.panels']
        if ViewGroupDebugPanel not in panels:
            panels.append(ViewGroupDebugPanel)
    except KeyError:
        raise KeyError("Did you include pyramid_debugtoolbar before including this?")

