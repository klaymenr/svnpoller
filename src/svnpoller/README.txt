`svnpoller` watches target SVN repositories regularly and transmits a
commit-mail to the designated notify party about each commit when there
are new commits.

Requirements
------------

* Python 2.6 or later


Dependencies
------------

* `setuptools <http://pypi.python.org/pypi/setuptools>`_ or
  `distribute <http://pypi.python.org/pypi/distribute>`_

* `lxml`

* svn external command (1.6 or later)


Features
--------

* polling specified svn repository

* send commit message and diff by email


Setup
-----

Make environment (by easy_install)::

   $ easy_install svnpoller


Make environment (by buildout)::

   $ hg clone http://bitbucket.org/shimizukawa/svnpoller
   $ cd svnpoller
   $ python bootstrap.py
   $ bin/buildout


Copy and modify ini file. example::

   $ cp <svnpoller installed path>/svnpoller/svnpoller.ini .
   $ vi svnpoller.ini

Usage
-----

Execute svnpoller command::

   $ svnpoller svnpoller.ini

or setup cron job::

   $ crontab -e
   0 0 * * * /path/to/svnpoller /path/to/svnpoller.ini


History
-------

0.0.1
~~~~~
* first release

