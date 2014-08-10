=====
Usage
=====

.. important::

   We assume at this stage that you already read and understand the part of
   the |rf-user-guide| dedicated to tests suite authors.

About ``Selenium2Library``
==========================

The only |robotframework| library exposed by **robotframework-drupallibrary**
is called :obj:`DrupalLibrary`. Using its keywords in any test case requires
to setup and open a browser using its :obj:`Open Browser` keyword.

Indeed, :obj:`DrupalLibrary` keywords use the Selenium browser instance that
is peovided by :obj:`Selenium2Library`. And running any :obj:`DrupalLibrary`
without having previously opened a :obj:`Selenium2Library` browser may drive
to unpredictable results and behaviour.

Demos
=====

Demo files are provided in the :file:`demos/` folder of the source bundle
distributed in our Git repository. Here are some of them that you could use as
a starter for your test suites.

.. hint::

   Please read the :download:`DrupalLibrary keywords <robot-doc.html>` in
   another browser window while reading the demos code.

The resources
-------------

The common resources are provided by the file :file:`resources.robot`. It just
defines a set of variables and an utility keyword.

.. literalinclude:: ../demos/resources.robot
   :language: robotframework

Adding members
--------------

The suite from the file :file:`addmembers.robots` adds - as its name says - 3
members, using the :obj:`Sign In` and :obj:`Add Member` keywords provided by
:obj:`DrupalLibrary`. As you can notice as warned above, the suite opens a
browser with the :obj:`Open Browser` keyword from the :obj:`Selenium2Library`.

.. literalinclude:: ../demos/addmembers.robot
   :language: robotframework

Removing these members
----------------------

The suite from the file :file:`removemembers.robot` removes the member
previously added in various fashions.

.. literalinclude:: ../demos/removemembers.robot
   :language: robotframework

Running the demos
-----------------

.. attention::

   Don't forget to activate your ``robots`` virtualenv before running these
   commands. See the :ref:`installation` chapter.

   The test suite targets a public Drupal 7 demo site. You may prefer using
   your own development site changing the variables :samp:`${HOME URL}`
   alonside with :samp:`${WM NAME}` (the username of an administrator) and
   :samp:`${WM PASS}` (his password).

Of course you start with :file:`addmembers.robot` :

.. code-block:: console

   (robots)$ cd demos
   (robots)$ pybot addmember.robot
   ==============================================================================
   Addmembers :: Adding members to the Drupal demo site
   ==============================================================================
   Open Home Page                                                        | PASS |
   ------------------------------------------------------------------------------
   Signing In                                                            | PASS |
   ------------------------------------------------------------------------------
   Adding Some Members                                                   | PASS |
   ------------------------------------------------------------------------------
   Attempt To Duplicate A Member :: We know johndoe is already regist... | FAIL |
   Something went wrong when creating user johndoe. (Have been waiting for 5 seconds)
   ------------------------------------------------------------------------------
   Addmembers :: Adding members to the Drupal demo site                  | FAIL |
   4 critical tests, 3 passed, 1 failed
   4 tests total, 3 passed, 1 failed
   ==============================================================================
   Output:  /Users/glenfant/projets/robotframework-drupallibrary/demos/output.xml
   Log:     /Users/glenfant/projets/robotframework-drupallibrary/demos/log.html
   Report:  /Users/glenfant/projets/robotframework-drupallibrary/demos/report.html

The console log reports briefly the test session in :file:`log.html` and
:file:`report.html`.

:file`report.html` provides a per suite summary of the run. Links are provided
:to the details published in :file:`log.html`.

You can notice that the failure details in :file:`log.html` shows the browser
screenshot at the moment of the failure.

In addition an file named :file:`output.xml` is issued by the session. It
carries the equivalent informations of the ones provided by
:file:`report.html` you can parse in a custom QA application.

.. note::

   :file:`output.xml` is not suitable to Jenkins PIC. Use the ``--xunit``
   option to provide a Jenkins suitable report file.

   Type :command:`rebot --help` to display some usages of this
   :file:`output.xml` file.

Now let's remove our users:

.. code-block:: console

   (robots)$ pybot removemembers.robot
   ==============================================================================
   Removemembers :: Remove members added by the addmembers.robot suite
   ==============================================================================
   Open Home Page                                                        | PASS |
   ------------------------------------------------------------------------------
   Signing In                                                            | PASS |
   ------------------------------------------------------------------------------
   Removing Some Members                                                 | PASS |
   ------------------------------------------------------------------------------
   Attempt to remove a unknown user                                      | FAIL |
   KeywordError: It seems there is no user named nosuchanuser
   ------------------------------------------------------------------------------
   Removemembers :: Remove members added by the addmembers.robot suite   | FAIL |
   4 critical tests, 3 passed, 1 failed
   4 tests total, 3 passed, 1 failed
   ==============================================================================
   Output:  /Users/glenfant/projets/robotframework-drupallibrary/demos/output.xml
   Log:     /Users/glenfant/projets/robotframework-drupallibrary/demos/log.html
   Report:  /Users/glenfant/projets/robotframework-drupallibrary/demos/report.html

As in the previous session new :file:`output.xml`, :file:`log.html` and
:file:`report.html` files have been created. Comments about these files are
superfluous since the above discussion says all at that level.
