from betahaus.viewcomponent import view_action

@view_action('group', 'one')
@view_action('group', 'two')
@view_action('group', 'three')
def name_action(context, request, va):
    return va.name


def includeme(config):
    config.scan(__name__)
