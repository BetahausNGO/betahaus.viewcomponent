from pyramid.testing import DummyResource

from zope.interface import Interface
from zope.interface import implements


class IRoot(Interface):
    pass

class IOrganisation(Interface):
    pass


class Root(DummyResource):
    implements(IRoot)

class Organisation(DummyResource):
    implements(IOrganisation)
