.. _api:

===
API
===

User API
========

The user API doc is generated automatically with the command:

.. code-block:: console

   python -m robot.libdoc DrupalLibrary the-doc.html

.. hint::

   Open the :download:`User API documentation <robot-doc.html>` in a new tab
   or window to keep the focus here.

Python API
==========

This API is intended to be used by third party Python application authors who
want to leverage **robotframework-drupallibrary**. You don't need to read this
if you're a QA engineer who just want to use it.

Subclassing is evil
-------------------

Never subclass the ``DrupalLibrary`` class. It won't work as expected:

.. code-block:: python

   from DrupalLibrary import DrupalLibrary

   # This is evil
   class MyDrupalLibrary(DrupalLibrary):
      # Whatever...

As said elsewhere, we need to share the same Selenium browser instance as
``Selenium2Library``, unless we may have unpredictable behaviours. And your
library should do it too.

Consider re-using its resources like in this pattern:

.. code-block:: python

   from robot.libraries.BuiltIn import BuiltIn

   class MyDrupalLibrary(object)

       def __init__(self, whatever, other, initializers):

           self.drupallib = Builtin().get_library_instance('DrupalLibrary')
           # Other init code ...

       def new_keyword(self, whatever):
           """Your custome keyword"""
           self.drupallib.go_home()  # Re-using DrupalLibrary keyword

       def __getattr__(self, name):
           """Delegate to the DrupalLibrary instance methods unknown here"""
           if hasattr(self.drupallib, name):
               return getattr(self.drupallib, name)
           else:
               err_msg = "Neither MyDrupalLibrary nor DrupalLibrary have {0} attribute".format(name)
               raise AttributeError(err_msg)

DrupalLibrary methods
---------------------

Check the source code and the :download:`User API documentation
<robot-doc.html>`. You just need to know that a Python method named ``foo_bar`` is
automatically available as ``Foo Bar`` keyword.

Other "non keyword" methods are explained below in the base class of
:class:`DrupalLibrary`:

.. autoclass:: DrupalLibrary.DrupalKeywords
   :members: _wait_bo_ok_status, _actual_html, _selenium_browser
