.. _installation:

============
Installation
============

Common Prerequisites
====================

I assume that you already got Python 2.7, the |pip| installer and - preferably
bet not necessarily - |virtualenv|.

.. attention::

   Unlike lots of |robotframework| libraries, this package will work only with
   CPython, and not Jython or IronPython.

   Why ? Because explore in depth complex HTML structures as the ones
   distributed by modern CMS need a real HTML parser with the support of a
   full featured XPath engine. That's why I use the excellent |lxml| package,
   that does not - unfortunately - support Jython or IronPython.

End user installation
=====================

If you just want to use **robotframework-drupallibrary**, you may add and
activate a dedicated |virtualenv| (strongly recommended) before installing it:

.. code-block:: console

   $ mkdir ~/venvs
   $ cd ~/venvs
   $ virtualenv robots
   $ source robots/bin/activate
   (robots)$

.. note::

   Of course you may replace above labels ``venvs`` and ``robots`` with what
   you'd prefer. This is just an example, but adapt further reading to your
   alternate choice.

As of today, **robotframework-drupallibrary** is not yet released as a package
at |PyPI|, so you'll install at the moment from the Git repository:

.. code-block:: console

   (robots)$ pip install -e git+https://github.com/alterway/robotframework-drupallibrary#egg=robotframework-drupallibrary

OK, you're done. Continue reading with the next chapter.

.. _developer_installation:

Developer installation
======================

If you're intended to use and contribute to **robotframework-drupallibrary**,
follow these steps :

.. code-block:: console

   (robots)$ git clone git@github.com:alterway/robotframework-drupallibrary.git
   (robots)$ cd robotframework-drupallibrary
   (robots)$ python setup.py develop

Install the development and tests specific add-ons:

.. code-block:: console

   (robots)$ pip install robotframework-drupallibrary[dev]

Building this documentation
---------------------------

.. code-block:: console

   (robots)$ python setup.py build_sphinx

The HTML documentation is now available in the directory mentioned by the
:file:`setup.cfg` in the ``build_dir`` option of the ``build_sphinx`` section.

Running the tests
-----------------

.. code-block:: console

   (robots)$ python setup.py test

.. note::

   If you're working on a Git fork, your "pull request" won't be accepted if
   you don't keep the tests smiling.
