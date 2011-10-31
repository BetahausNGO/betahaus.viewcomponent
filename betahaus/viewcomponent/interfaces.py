from zope.interface import Attribute
from zope.interface import Interface


class IViewGroup(Interface):
    """ A dict-like utility that will contain ViewAction objects.
        There are a few differences from normal dictionaries.

        * It can only contain ViewAction objects
        * It's ordered (with the order-attribute)
        * It's callable

        You normally won't add these yourself, but rather use the decorator
        view_action which will create ViewGroup utilities as needed.

        Below, we use the followong names:
        * view_group is an instantiated ViewGroup object.
        * view_action is an instantiated ViewAction object. (I.e. not the decorator)
    """
    name = Attribute("""
        Name of this ViewGroup. It's not needed, but it makes debugging a lot easier.
        The decorator will set the name when it registers the adapter. The name will be
        the same as the utility name.""")

    order = Attribute("""
        A property which will return a tuple of the set order. You can change the order
        by assigning a list to it. Any keys that exist but aren't in the assigned list
        will be added last.""")

    perm_checker = Attribute("""
        Permission checker, usually Pyramids has_permission.
        You can add any other callable here if you want, but it must accept the same
        arguments as Pyramids version, i.e. permission, context, request.
        See pyramid.security.has_permission for more info.""")

    def __init__(name = None, perm_checker = None):
        """ Initialize, accepts permission checker as argument which will default
            to Pyramids version if None is supplied.
        """
    
    def __call__(context, request, **kw):
        """ Return a list with the output of each contained view action.
            Call will also catch exceptions and add a bit extra information
            to them so it's easier to identify where it came from.
            (Tracebacks can otherwise be kind of weird, especially from nested view groups)
        """

    def __getitem__(key):
        """ Normal dict interface """

    def __setitem__(key, value):
        """ Normal dict interface """

    def __delitem__(key):
        """ Normal dict interface """

    def __len__():
        """ Number of contained ViewAction objects. """

    def __contains__(key):
        """ To implement dict interface with 'in' command, example:
            >>> 'logo' in view_group
            True
        """

    def get_context_vas(context, request):
        """ Return a generator with the ViewAction objects, without calling them
        """

    def add(view_action):
        """ Add a ViewAction object. It will be added with it's name attribute
            as key.
            This is the same as doing the followin:
            >>> view_group['name'] = view_action
        """

    def get(key, default=None):
        """ Same as dict get """

    def keys():
        """ Same as normal dict, but ordered. """

    def values():
        """ Same as normal dict, but ordered. """

    def items():
        """ Same as normal dict, but ordered. """
