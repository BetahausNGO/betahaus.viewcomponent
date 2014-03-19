Changes
=======


0.3b / (2014-03-19)
-------------------

- View groups don't catch exceptions any longer. This was a cause of a lot of
  odd error messages on Python 2.
- Ordering with bad keys don't cause exceptions - they're logged as warnings instead.
- New argument priority for view actions. [ixmatus]


0.2b (2013-06-18)
-----------------

-  Python3 support fixed by pib (Paul Bonser) - thanks a lot!
-  Fetch and execution of vas changed - empty result should be ignored,
   and yield isn't used now. This should make error messages clearer. [robinharms]
-  Checks for containment, interface, permission etc moved to ViewAction object, since
   they weren't performed if the object was called directly. [robinharms]


0.1b
----

-  Initial version
