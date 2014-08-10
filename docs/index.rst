.. _index:

============================
robotframework-drupallibrary
============================

This package provides a set of keywords that help ATDD testing of Drupal based
sites using the great |robotframework| Acceptance Test Driven Development
toolset.

You need to automate acceptance tests on a Drupal site target with
|robotframework| like this:

.. code-block:: robotframework

   *** Settings ***
   Library Selenium2Library
   Library DrupalLibrary    ${HOME_PAGE}

   *** Variables ***
   ${HOME_PAGE}     http://localhost/drupal

   *** Test Cases ***
   Go Home As Admin
       Log Out
       Sign In    admin  secret
       Go Home

You're at a good place.

.. attention::

   This package is alphaware and still actively at work. The APIs and
   `RobotFramework`_ keywords exposed may change quickly depending on users
   feedbacks.

   Of course, :ref:`contributing` to this package in order to have a full
   featured and robust support of Drupal is welcome.

Contents
========

.. toctree::
   :maxdepth: 2

   overview
   installation
   usage
   api
   contributing
   resources
   contributors
   changes

Indexes and tables
==================

* :ref:`genindex`
* :ref:`search`
