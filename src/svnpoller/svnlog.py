# -*- coding: utf-8 -*-

__all__ = ['POPEN_KW', 'Log', 'get_logs', 'get_log', 'get_revisions']


import os, subprocess
from datetime import datetime
try:
    # for python 2.5 or later.
    from xml.etree.ElementTree import fromstring as xml2elem
except:
    try:
        # for python 2.4. need lxml
        from lxml.etree import XML as xml2elem
    except:
        raise ImportError("Need 'xml.etree.ElementTree.fromstring' or 'lxml.etree.XML'")

POPEN_ENV = os.environ.copy()
POPEN_ENV['LANG'] = 'C'

POPEN_KW = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=POPEN_ENV)



class Log(object):
    def __init__(self, url, rev):
        self.url = url
        self.rev = rev

        xml_data = self._prepare_info(self.url, self.rev)
        root = xml2elem(xml_data)
        entry = root.find('entry')
        self.url = entry.find('url').text
        self.root = entry.find('repository').find('root').text
        self.subpath = self.url[len(self.root):]

        xml_data = self._prepare_log(self.url, self.rev)
        root = xml2elem(xml_data)
        entry = root.find('logentry')
        self.paths = [(x.attrib['action'], x.text) for x in entry.find('paths')]
        #self.normalized_paths = [
        #        (a, p[len(self.subpath):].lstrip('/'))
        #        for a,p in self.paths]
        self.author = entry.find('author').text
        self.date = datetime.strptime(entry.find('date').text[:19],'%Y-%m-%dT%H:%M:%S')
        self.msg = entry.find('msg').text
        self.diff = self._prepare_diff(self.url, self.rev)

    def _prepare_info(self, url, rev):
        cmd = ['svn', 'info', '--xml']
        cmd.append('-r%s' % str(rev))
        cmd.append(url)
        out,err = command(cmd)
        return out

    def _prepare_log(self, url, rev):
        cmd = ['svn', 'log', '-v', '--xml']
        cmd.append('-r%s' % str(rev))
        cmd.append(url)
        out,err = command(cmd)
        return out

    def _prepare_diff(self, url, rev):
        cmd = ['svn', 'diff']
        cmd.append('-c%s' % rev)
        cmd.append(url)
        out,err = command(cmd)
        return out

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
    cmd = ['svn', 'log', '--xml']
    if rev and rev2:
        cmd.append('-r%s:%s' % (str(rev), str(rev2)))
    elif rev:
        cmd.append('-c%s' % str(rev))
    cmd.append(url)
    out,err = command(cmd)
    root = xml2elem(out)
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
        cmd = ['svn', 'log', '--xml']
        if rev:
            cmd.append('-r%s:HEAD' % str(rev))
        cmd.append(url)
        out,err = command(cmd)
        root = xml2elem(out)
        revs.update(int(node.attrib['revision']) for node in root)

    return sorted(revs)

def command(cmd):
    proc = subprocess.Popen(cmd, **POPEN_KW)
    out,err = proc.communicate()
    proc.wait()
    return out,err

