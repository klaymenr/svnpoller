import os, sys, subprocess
from ConfigParser import SafeConfigParser
from StringIO import StringIO
from lxml import etree

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svnpoller.ini')
DEFAULTS = dict(url=None, address=None, newest_rev=None)

ENV = os.environ.copy()
ENV['LANG'] = 'C'

POPEN_KW = dict(stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=ENV)


def run(*args, **kw):
    conf = SafeConfigParser(DEFAULTS)
    conf.read(CONFIG_PATH)
    for sect in conf.sections():
        svn_log = ['svn', 'log', '--xml']
        newest_rev = conf.get(sect, 'newest_rev')
        if newest_rev:
            svn_log.append('-r%d:HEAD' % (int(newest_rev)+1))
        svn_log.append(conf.get(sect, 'url'))
        proc = subprocess.Popen(svn_log, **POPEN_KW)
        xml_data = proc.stdout.read()

        root = etree.XML(xml_data)
        for node in reversed(root):
            rev = node.attrib['revision']
            svn_diff = ['svn', 'diff']
            svn_diff.append('-c%s' % rev)
            svn_diff.append(conf.get(sect, 'url'))
            proc = subprocess.Popen(svn_diff, **POPEN_KW)
            diff_data = proc.stdout.read()
            print '---------------'
            print ' Revision: %s' % rev
            print ' Author: %s' % node.find('author').text
            print ' Date: %s' % node.find('date').text
            print ' Message:'
            print node.find('msg').text
            print
            print diff_data
            conf.set(sect, 'newest_rev', rev)

    conf.write(open(CONFIG_PATH, 'wt'))

