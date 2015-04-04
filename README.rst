.. image:: https://travis-ci.org/robinharms/betahaus.viewcomponent.png?branch=master
  :target: https://travis-ci.org/robinharms/betahaus.viewcomponent

betahaus.viewcomponent README
=============================

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

You may optionally use a directive of the config object.
You need to include ``betahaus.viewcomponent`` in that case.

.. code-block:: python

   #Code in your package
   
   def logo_tag(context, request, va):
       return '<img src="img.png" />'
   
   def includeme(config):
       config.add_view_action(logo_tag, 'stuff', 'logo')


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
       return '<li><a href="/login">Login</a></li>'
   
   @view_action('menu', 'logout')
   def logout_link(context, request, va):
       return '<li><a href="/logout">Logout</a></li>'
   
   @view_action('menu', 'my_personal_stuff', permission = 'ViewStuff')
   def personal_link(context, request, va):
       """ This will only render if user has permission 'ViewStuff'"""
       return '<li><a href="/my-stuff">My stuff</a></li>'

After your app has been started, you'll have a menu now. Also, other apps may add to it the same way,
or remove your initial alternatives.


Advanced example - a pluggable json renderer
--------------------------------------------

Usecase: You pull JSON from a database. Some information is sensitive
and should only be visible to some users. Other plugins want to be able
to attach or change information to the JSON response.

Our context will be a mock user object where the email
field is to be treated as sensitive information.

.. code-block:: python

   class User(object):
       userid = ""
       email = ""

   #etc...
 
First, add two view actions for userid and email. The email one will have the permission
``Show secret``.

.. code-block:: python

   from betahaus.viewcomponent import view_action
   
   @view_action('json', 'userid')
   def get_userid(context, request, va, **kw):
       return getattr(context, 'userid', '')
   
   @view_action('json', 'email', permission = 'Show secret')
   def get_email(context, request, va, **kw):
       return getattr(context, 'email', '')

Second, lets register a regular view, that will return the view group ``json``.

.. code-block:: python

   from betahaus.viewcomponent import render_view_group
   from pyramid.view import view_config
   
   @view_config(context = 'User', renderer = 'json', name = 'user.json')
   def user_view(context, request):
       """ Render json."""
       return render_view_group(context, request, 'json', as_type='dict', empty_val = '')

Email will now only be included if the user/thing requesting the view
has the ``Show secret`` permission.
The ``as_type`` argument will render the view results as a dict where the keys
will be the view actions name. (user and email in this case)
``empty_val`` specifies that any None or empty strings returned should be replaced by this value.
So even if userid returns '', that value will still be included.


Bonus: Spacer
-------------

Spacer will be added when the view action output is joined as a string,
the default behaviour. It's the same thing as doing spacer.join([view1, view2, etc])


Bonus: Priority
---------------

The priority argument sets the order when a view action is added.
Priority is sorted acending, so 10 is called before 20.


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
