from betahaus.viewcomponent import view_action


@view_action('group', 'action')
def _callme(*args):
    return "".join([str(x) for x in args])

@view_action('html', 'stuff')
def _callable_html(context, request, va):
    return "%s, %s, %s" % (context.__class__, request.__class__, str(va))


def includeme(config):
    config.scan(__name__)
