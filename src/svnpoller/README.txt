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

* send commit message and diff by email


An example
----------

Make environment (by easy_install)::

   $ easy_install svnpoller


Make environment (by buildout)::

   $ hg clone http://bitbucket.org/shimizukawa/svnpoller
   $ cd svnpoller
   $ python bootstrap.py
   $ bin/buildout


Copy and write ini file. example::

   $ cp <svnpoller installed path>/svnpoller/svnpoller.ini .
   $ svnpoller svnpoller.ini


History
-------

0.0.1
~~~~~
* first release

