.. betahaus.viewcomponent documentation master file, created by
   sphinx-quickstart on Sun Oct 30 14:09:50 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

betahaus.viewcomponent
======================

Reusable components in web pages make them a lot more fun and rewarding to write.
The goal of this package is to make them easy to add, remove and change.
While it's usable in a regular webapp, it's probably more interesting to use
in something that others will extend or change, like a framework.

It's written to be flexible and easy to adapt, rather than being the perfect solution to everything.


Basic example - adding a logo
-----------------------------

First, create a method that returns an html tag.
We also need to decorate this method.
The va positional argument is a ViewAction - we can ignore that
in this example.

.. code-block:: python

    from betahaus.viewcomponent import view_action
    @view_action('stuff', 'logo')
    def logo_tag(context, request, va):
        return '<img src="img.png" />'

When you run ``config.scan('your-apps-name')`` with this code present,
it will create a ViewGroup with the name 'stuff', that has a ViewAction
called 'logo'.

The ViewGroup is an ordered dict-like Utility, that keeps track of ViewActions.

If you want to get the result of a ViewGroup, simply do this:

.. code-block:: python

    from betahaus.viewcomponent import render_view_group
    render_view_group(context, request, 'stuff')

Since there's nothing else in this ViewGroup, only the logo tag will be returned.

To get the result of a single ViewAction only, you can call ``render_view_action``:

.. code-block:: python

    from betahaus.viewcomponent import render_view_action
    render_view_action(context, request, 'stuff', 'logo')


Another example - building a menu
---------------------------------

So you have a webapp, and you want a menu somewhere. And then package X, Y and Z
works as plugins, but how do they add to that menu of yours?
(Read the Pyramid docs on how to create views)

First, let's create minimal Python view code:

.. code-block:: python

    from betahaus.viewcomponent import render_view_group
    from pyramid.view import view_config
    
    @view_config(renderer = 'some/template.pt')
    def main_template(context, request):
        return dict(render_view_group = render_view_group)
      
And then the template:

.. code-block:: html

    <html>
      <body>
        <ul>${render_view_group(context, request, 'menu')}</ul>
      </body>
    </html>

The menu will be simple html strings, a ``<li>`` for each statement.
To return them, we need decorated methods. Note that the ViewGroup
``menu`` will be created as soon as it's populated. (the first argument in the decorator)

.. code-block:: python

    from betahaus.viewcomponent import view_action


    @view_action('menu', 'login')
    def login_link(context, request, va):
        return "<li><a href="/login">Login</a></li>"

    @view_action('menu', 'logout')
    def logout_link(context, request, va):
        return "<li><a href="/logout">Logout</a></li>"

    @view_action('menu', 'my_personal_stuff', permission = 'ViewStuff')
    def personal_link(context, request, va):
        """ This will only render if user has permission 'ViewStuff'"""
        return "<li><a href="/my-stuff">My stuff</a></li>"

After your app has been started, you'll have a menu now. Also, other apps may add to it the same way,
or remove your initial alternatives.

For full documentation of each method, please see interfaces.py.


Installing debug panel
----------------------

To see which view components that are registered and active, this package comes with a debug panel, ment to be used with
`Pyramid Debug toolbar <http://docs.pylonsproject.org/projects/pyramid_debugtoolbar/en/latest/>`_.
Include that package before including this debug panel. Usually something like this in your paster.ini file:

.. code-block:: text

    pyramid.includes =
        pyramid_debugtoolbar
        betahaus.viewcomponent.debug_panel

The panel will now display realtime information on active components, and where you can find their modules.


Requirements
------------

This package currently isn't usable outside of `Pyramid <http://www.pylonsproject.org/>`_, but it could be
changed to be more generic and only require the basic `Zope Component Architechture <http://www.muthukadan.net/docs/zca.html>`_ .
It also depends on venusian, which will be fetched by Pyramid.


Feedback and features
---------------------

The source code of the package is really small, and it should be commented enough so it's
easy to pick up what to do with it. The package is still under development, but used on several
production servers today.

If you have suggestions, criticism, feedback, ideas - please don't hesitate to contact me
or add an `issue at GitHub <https://github.com/robinharms/betahaus.viewcomponent/issues>`_.


Changes and credits
===================

.. toctree::
   :maxdepth: 1

   CHANGES
   CREDITS


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :hidden:
   
   api