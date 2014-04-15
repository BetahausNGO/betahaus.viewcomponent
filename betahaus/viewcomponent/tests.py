from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from betahaus.viewcomponent.interfaces import IViewAction
from betahaus.viewcomponent.interfaces import IViewGroup
from betahaus.viewcomponent.fixtures import contexts


def _dummy_callable(*args):
    return "".join([str(x) for x in args])

def _callable_text(context, request, va):
    return "%s, %s, %s" % (context.__class__, request.__class__, str(va))

def _name_callable(context, request, va):
    return va.name

def _bad_callable(*args):
    return TestCase

def _failing_callable(*args):
    raise Exception('Buhu!')

def _none_callable(*args):
    pass


class ViewGroupTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.viewcomponent.models import ViewGroup
        return ViewGroup

    @property
    def _view_action(self):
        from betahaus.viewcomponent.models import ViewAction
        return ViewAction

    def test_verify_class(self):
        self.failUnless(verifyClass(IViewGroup, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(IViewGroup, self._cut()))

    def test_add(self):
        obj = self._cut()
        va = self._view_action(_dummy_callable, 'name')
        obj.add(va)
        self.failUnless('name' in obj)

    def test_add_sets_parent(self):
        obj = self._cut()
        va = self._view_action(_dummy_callable, 'name')
        obj.add(va)
        self.assertEqual(va.parent, obj)

    def test_del(self):
        obj = self._cut()
        va = self._view_action(_dummy_callable, 'name')
        obj.add(va)
        self.failUnless('name' in obj) #To make sure
        del obj['name']
        self.failIf('name' in obj)

    def test_len(self):
        obj = self._cut()
        va = self._view_action(_dummy_callable, 'name')
        obj.add(va)
        self.assertEqual(len(obj), 1)

    def test_call(self):
        obj = self._cut()
        va = self._view_action(_dummy_callable, 'name')
        obj['va'] = va
        self.assertEqual(obj('context', 'request'), "contextrequest<betahaus.viewcomponent.models.ViewAction 'name'>")

    def test_call_no_va(self):
        obj = self._cut()
        self.assertEqual(obj('context', 'request'), '')

    def test_call_bad_output_from_va(self):
        obj = self._cut()
        va = self._view_action(_bad_callable, 'name')
        obj.add(va)
        self.assertRaises(TypeError, obj, None, None)

    def test_call_empty_output(self):
        obj = self._cut()
        va = self._view_action(_none_callable, 'this_view_group')
        obj.add(va)
        self.assertEqual(obj(None, None), u"")

    def test_default_order(self):
        obj = self._cut()
        obj.add(self._view_action(_dummy_callable, 'one'))
        obj.add(self._view_action(_dummy_callable, 'two'))
        self.assertEqual(obj.order, ['one', 'two'])

    def test_set_order(self):
        obj = self._cut()
        obj.add(self._view_action(_dummy_callable, 'one'))
        obj.add(self._view_action(_dummy_callable, 'two'))
        obj.order = ['two', 'one']
        self.assertEqual(obj.order, ['two', 'one'])

    def test_order_respected_on_call(self):
        obj = self._cut()
        obj.add(self._view_action(_name_callable, 'one'))
        obj.add(self._view_action(_name_callable, 'two'))
        obj.order = ['two', 'one']
        context = None
        request = None
        self.assertEqual(obj(context, request), 'twoone')

    def test_order_bad_key(self):
        obj = self._cut()
        obj.add(self._view_action(_name_callable, 'one'))
        obj.add(self._view_action(_name_callable, 'two'))
        obj.order = ['one', '404', 'two', 'none']
        self.assertEqual(obj.order, ['one', 'two'])

    def test_set_order_with_some_keys_left_out(self):
        obj = self._cut()
        obj.add(self._view_action(_name_callable, 'one'))
        obj.add(self._view_action(_name_callable, 'two'))
        obj.order = ['two']
        #one should be appended as well
        self.assertEqual(obj.order, ['two', 'one'])

    def test_get(self):
        obj = self._cut()
        va = self._view_action(_dummy_callable, 'hello')
        obj.add(va)
        self.assertEqual(obj.get('hello'), va)

    def test_keys_respect_order(self):
        obj = self._cut()
        obj.add(self._view_action(_name_callable, 'one'))
        obj.add(self._view_action(_name_callable, 'two'))
        obj.add(self._view_action(_name_callable, 'three'))
        obj.order = ['three', 'one']
        self.assertEqual(obj.keys(), ['three', 'one', 'two'])

    def test_values_respect_order(self):
        obj = self._cut()
        va1 = self._view_action(_name_callable, 'one')
        va2 = self._view_action(_name_callable, 'two')
        va3 = self._view_action(_name_callable, 'three')
        obj.add(va1)
        obj.add(va2)
        obj.add(va3)
        obj.order = ['three', 'one']
        self.assertEqual(obj.values(), [va3, va1, va2])

    def test_items_respect_order(self):
        obj = self._cut()
        va1 = self._view_action(_name_callable, 'one')
        va2 = self._view_action(_name_callable, 'two')
        va3 = self._view_action(_name_callable, 'three')
        obj.add(va1)
        obj.add(va2)
        obj.add(va3)
        obj.order = ['three', 'one']
        self.assertEqual(obj.items(), [('three', va3), ('one', va1), ('two', va2)])

    def test_deleted_resource_removed_from_order(self):
        obj = self._cut()
        va1 = self._view_action(_name_callable, 'one')
        va2 = self._view_action(_name_callable, 'two')
        obj.add(va1)
        obj.add(va2)
        obj.order = ['two', 'one']
        del obj['two']
        self.assertEqual(obj.order, ['one'])

    def test_priority_respected(self):
        obj = self._cut()
        va1 = self._view_action(_name_callable, 'one', priority = 1)
        va2 = self._view_action(_name_callable, 'two', priority = 10)
        va3 = self._view_action(_name_callable, 'three', priority = 5)
        obj.add(va1)
        obj.add(va2)
        obj.add(va3)
        self.assertEqual(obj.items(), [('one', va1), ('three', va3), ('two', va2)])
        self.assertEqual(obj.order, ['one', 'three', 'two'])

    def test_priority_equal_values(self):
        obj = self._cut()
        va1 = self._view_action(_name_callable, 'one', priority = 1)
        va2 = self._view_action(_name_callable, 'two', priority = 2)
        va3 = self._view_action(_name_callable, 'three', priority = 1)
        obj.add(va1)
        obj.add(va2)
        obj.add(va3)
        self.assertEqual(obj.items(), [('one', va1), ('three', va3), ('two', va2)])
        self.assertEqual(obj.order, ['one', 'three', 'two'])

    def test_priority_specified_mixed_with_no_value(self):
        obj = self._cut()
        va1 = self._view_action(_name_callable, 'one')
        va2 = self._view_action(_name_callable, 'two', priority = 2)
        va3 = self._view_action(_name_callable, 'three', priority = 1)
        obj.add(va1)
        obj.add(va2)
        obj.add(va3)
        self.assertEqual(obj.items(), [('three', va3), ('two', va2), ('one', va1)])
        self.assertEqual(obj.order, ['three', 'two', 'one'])


class ViewActionTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.viewcomponent.models import ViewAction
        return ViewAction

    def _dummy_vg(self, perm_checker = None):
        from betahaus.viewcomponent.models import ViewGroup
        return ViewGroup(name = 'dummy', perm_checker = perm_checker)

    def test_verify_class(self):
        self.failUnless(verifyClass(IViewAction, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(IViewAction, self._cut(_dummy_callable, 'name')))

    def test_callable(self):
        obj = self._cut(_dummy_callable, 'name')
        self.assertEqual(obj('hello', 'world'), "helloworld<betahaus.viewcomponent.models.ViewAction 'name'>")

    def test_call_no_restriction(self):
        obj = self._cut(_name_callable, 'name')
        context = testing.DummyModel()
        request = testing.DummyRequest()
        self.assertEqual(obj(context, request), 'name')

    def test_call_with_perm_allow(self):
        def _ck_true(*args):
            return True
        vg = self._dummy_vg(_ck_true)
        obj = self._cut(_name_callable, 'allow', permission = 'Dummy')
        vg.add(obj)
        context = testing.DummyModel()
        request = testing.DummyRequest()
        self.assertEqual(obj(context, request), 'allow')

    def test_call_with_perm_deny(self):
        def _ck_false(*args):
            return False
        vg = self._dummy_vg(_ck_false)
        obj = self._cut(_name_callable, 'deny', permission = 'Dummy')
        vg.add(obj)
        context = testing.DummyModel()
        request = testing.DummyRequest()
        self.assertEqual(obj(context, request), None)

    def test_call_with_interface_allow(self):
        obj = self._cut(_name_callable, 'allow', interface = contexts.IRoot)
        context = contexts.Root()
        request = testing.DummyRequest()
        self.assertEqual(obj(context, request), 'allow')

    def test_call_with_interface_deny(self):
        obj = self._cut(_name_callable, 'deny', interface = contexts.IOrganisation)
        context = contexts.Root()
        request = testing.DummyRequest()
        self.assertEqual(obj(context, request), None)

    def test_call_with_containment_allow(self):
        obj = self._cut(_name_callable, 'allow', containment = contexts.IRoot)
        root = contexts.Root()
        root['d'] = context = testing.DummyModel()
        request = testing.DummyRequest()
        self.assertEqual(obj(context, request), 'allow')

    def test_call_with_containment_deny(self):
        obj = self._cut(_name_callable, 'deny', containment = contexts.IOrganisation)
        root = contexts.Root()
        root['d'] = context = testing.DummyModel()
        request = testing.DummyRequest()
        self.assertEqual(obj(context, request), None)


class ViewActionDecoratorTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_dummy_picked_up_on_scan(self):
        self.config.include("betahaus.viewcomponent.fixtures.dummy")
        util = self.config.registry.getUtility(IViewGroup, name = 'group')
        res = util('context', 'request')
        self.assertEqual(res, "contextrequest<betahaus.viewcomponent.models.ViewAction 'action'>")


class RenderViewGroupTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _fut(self):
        from betahaus.viewcomponent import render_view_group
        return render_view_group

    def test_render_view_groups(self):
        request = testing.DummyRequest()
        context = testing.DummyResource()
        self.config.include("betahaus.viewcomponent.fixtures.dummy")
        res = self._fut(context, request, 'html')
        expected = "None, stuff"
        self.assertEqual(res, expected)


class RenderViewActionTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _fut(self):
        from betahaus.viewcomponent import render_view_action
        return render_view_action

    def test_render_view_action(self):
        request = testing.DummyRequest()
        context = testing.DummyResource()
        self.config.include("betahaus.viewcomponent.fixtures.group")
        res = self._fut(context, request, 'group', 'one')
        expected = "one"
        self.assertEqual(res, expected)
