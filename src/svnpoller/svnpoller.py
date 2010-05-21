import os, sys, subprocess
from urlparse import urlparse, urlunparse
from ConfigParser import ConfigParser
from StringIO import StringIO
from lxml import etree
import sendmail

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svnpoller.ini')

ENV = os.environ.copy()
ENV['LANG'] = 'C'

POPEN_KW = dict(stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=ENV)

MAIL_TEMPLATE = """\
* Revision: %(rev)s
* Author: %(auth)s
* Date: %(date)s
* Message:
%(msg)s

* Paths:
%(paths)s

* Diff:
%(diff)s
"""

def build_message(rev, auth, date, msg, paths, diff):
    return MAIL_TEMPLATE % locals()


class Log(object):
    def __init__(self, url, rev):
        self.url = url
        self.rev = rev
        self._prepare_log()
        self._prepare_diff()

    def _prepare_log(self):
        svn_log = ['svn', 'log', '-v', '--xml']
        svn_log.append('-r%s' % str(self.rev))
        svn_log.append(self.url)
        proc = subprocess.Popen(svn_log, **POPEN_KW)
        xml_data = proc.stdout.read()
        root = etree.XML(xml_data)
        entry = root.find('logentry')
        self.paths = [(x.attrib['action'], x.text) for x in entry.find('paths')]
        self.author = entry.find('author').text
        self.date = entry.find('date').text
        self.msg = entry.find('msg').text

    def _prepare_diff(self):
        svn_diff = ['svn', 'diff']
        svn_diff.append('-c%s' % self.rev)
        svn_diff.append(self.url)
        proc = subprocess.Popen(svn_diff, **POPEN_KW)
        self.diff = proc.stdout.read()

    def __repr__(self):
        return "<Log rev=%s, url='%s'>" % (str(self.rev), str(self.url))


def get_logs(url, rev=None, rev2=None):
    """
    >>> url = 'http://svn.example.com/repos/path'
    >>> get_logs(url, 1)
    [<Log rev=1, ...>]
    >>> get_logs(url, 1, 2)
    [<Log rev=1, ...>, <Log rev=2, ...>]
    >>> get_logs(url, 1, 3)
    [<Log rev=1, ...>, <Log rev=2, ...>, <Log rev=3>]
    >>> get_logs(url, 1, 'HEAD')
    [<Log rev=1, ...>, <Log rev=2, ...>, ..., <Log rev=10>]
    """
    svn_log = ['svn', 'log', '--xml']
    if rev and rev2:
        svn_log.append('-r%s:%s' % (str(rev), str(rev2)))
    elif rev:
        svn_log.append('-c%s' % str(rev))
    svn_log.append(url)
    proc = subprocess.Popen(svn_log, **POPEN_KW)
    xml_data = proc.stdout.read()
    root = etree.XML(xml_data)
    return [Log(url, node.attrib['revision']) for node in root]


def get_log(url, rev):
    return get_logs(url, rev)[0]


def get_revisions(urls, rev=None):
    """
    >>> urls = ['http://svn.example.com/repos/path1',
    ...         'http://svn.example.com/repos/path2']
    >>> get_revisions(urls)
    [1,2,3,5]
    >>> get_revisions(urls, 3)
    [3,5]
    """
    revs = set()
    for url in urls:
        svn_log = ['svn', 'log', '--xml']
        if rev:
            svn_log.append('-r%s:HEAD' % str(rev))
        svn_log.append(url)
        proc = subprocess.Popen(svn_log, **POPEN_KW)
        xml_data = proc.stdout.read()
        root = etree.XML(xml_data)
        revs.update(int(node.attrib['revision']) for node in root)

    return sorted(revs)


def run():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = CONFIG_PATH
    conf = ConfigParser()
    conf.read(config_file)

    mail_data = dict(
        smtpserver = conf.get('mail','smtpserver'),
        fromaddr = conf.get('mail','fromaddr'),
    )

    for sect in conf.sections():
        if sect == 'mail':
            continue

        opts = dict(conf.items(sect))

        newest_rev = opts.get('newest_rev', None)
        #if newest_rev: # add 1 rev
        #    newest_rev = str(int(newest_rev)+1)
        urls = filter(None, opts.get('url').splitlines())
        base_path = os.path.commonprefix([urlparse(x)[2].split('/')
                                          for x in urls])
        base_url = list(urlparse(urls[0]))
        base_url[2] = '/'.join(base_path)
        base_url = urlunparse(base_url)
        revs = get_revisions(urls, newest_rev)
        logs = [get_log(base_url, rev) for rev in revs]

        for log in logs:
            text = build_message(
                    log.rev, log.author, log.date, log.msg,
                    '\n'.join(" %s %s" % x for x in log.paths),
                    log.diff)

            rev = log.rev
            subject = '[%(sect)s: %(rev)s]' % locals()

            sendmail.send(
                    mail_data['fromaddr'],
                    opts.get('address'),
                    subject,
                    text,
                    smtpserver=mail_data['smtpserver'])

            conf.set(sect, 'newest_rev', rev)

    conf.write(open(config_file, 'wt'))

