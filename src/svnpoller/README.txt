`svnpoller` watches target SVN repositories regularly and transmits a
commit-mail to the designated notify party about each commit when there
are new commits.

Setting sample
--------------

svnpoller.ini::

   [mail]
   smtpserver = localhost
   fromaddr = admin@example.com

   [sample-section]
   url = http://svn.example.org/path/to/repos/with/sub/path
   address = test1@example.com, test2@example.com


Notify mail sample
-------------------

Notified mail sample::

   From: admin@example.com
   To: test1@example.com, test2@example.com
   Subject: [sample-section: 1230]

   * Revision: 1230
   * Author: foo
   * Date: 2009-11-22T17:40:47.287888Z
   * Message:
   The commit log message for this revision here.

   * Paths:
   M /with/sub/path/somefile1.py
   A /with/sub/path/somefile2.py

   * Diff:
   Index: somefile1.py
   ===================================================================
   --- somefile1.py     (revision 1230)
   +++ somefile1.py     (revision 1229)


Requirements
------------

* Python 2.4 or later


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

Please refer to `Setting sample`_ section for the format of the
`svnpoller.ini` configuration file.

Usage
-----

Execute svnpoller command::

   $ svnpoller svnpoller.ini

or setup cron job::

   $ crontab -e
   0 0 * * * /path/to/svnpoller /path/to/svnpoller.ini


History
-------

0.0.5
~~~~~
* Add changed `path-list` to mail-message.

0.0.4
~~~~~
* first release

