Changes
=======

0.4.1 (2015-04-04)
------------------

- Added: Option to return dict, generator or list instead of just joined strings.
- Added: Spacer option for the join statement.
- Added: A config directive ''add_view_action'' to att view actions without scanning.
- Fixed instance when replacing a ViewAction caused the new action to be displayed twice.
- Bugfix: When replacing, the order should be preserved unless priority is set.
- Removed debug panel since the code was outdated and didn't work with
  the newer version of pyramid_debugtoolbar

0.3.1b (2014-05-05)
-------------------

- Unicode wasn't an allowed string-type... (Brown paperbag for me) [robinharms]

0.3b (2014-03-19)
-----------------

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
