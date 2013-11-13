(unreleased)
------------

- Merged a fix from ixmatus (Parnell Springmeyer) so exception messages that aren't passed as args won't
  cause trouble. - thanks a lot!


0.2b
----

-  Python3 support fixed by pib (Paul Bonser) - thanks a lot!
-  Fetch and execution of vas changed - empty result should be ignored,
   and yield isn't used now. This should make error messages clearer. [robinharms]
-  Checks for containment, interface, permission etc moved to ViewAction object, since
   they weren't performed if the object was called directly. [robinharms]


0.1b
----

-  Initial version
