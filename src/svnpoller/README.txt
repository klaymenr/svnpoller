polling svn repository and notify by email.

Requirements
------------

* Python 2.6 or later


Dependencies
------------

* `setuptools <http://pypi.python.org/pypi/setuptools>`_ or
  `distribute <http://pypi.python.org/pypi/distribute>`_

* `lxml`

* svn command (1.6 or later)


Features
--------

* polling specified svn repository

* send commit log, diff by email


An example
----------

Make environment::

   $ easy_install svnpoller


Copy and write ini file. example::

   $ cp <svnpoller installed path>/svnpoller/svnpoller.ini .
   $ svnpoller svnpoller.ini


History
-------

0.0.1
~~~~~
* first release

