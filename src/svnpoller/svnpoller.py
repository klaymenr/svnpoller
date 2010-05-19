import os, sys, subprocess
from ConfigParser import ConfigParser
from StringIO import StringIO
from lxml import etree
import sendmail

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svnpoller.ini')

ENV = os.environ.copy()
ENV['LANG'] = 'C'

POPEN_KW = dict(stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=ENV)

MAIL_TEMPLATE = """
 Revision: %(rev)s
 Author: %(auth)s
 Date: %(date)s
 Message:
%(msg)s

%(diff)s
"""

def build_message(rev, auth, date, msg, diff):
    return MAIL_TEMPLATE % locals()


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

        svn_log = ['svn', 'log', '-v', '--xml']
        newest_rev = opts.get('newest_rev', None)
        if newest_rev:
            svn_log.append('-r%d:HEAD' % (int(newest_rev)+1))
        svn_log.append(opts.get('url'))
        proc = subprocess.Popen(svn_log, **POPEN_KW)
        xml_data = proc.stdout.read()

        root = etree.XML(xml_data)
        for node in reversed(root):
            rev = node.attrib['revision']
            svn_diff = ['svn', 'diff']
            svn_diff.append('-c%s' % rev)
            svn_diff.append(opts.get('url'))
            proc = subprocess.Popen(svn_diff, **POPEN_KW)
            diff_data = proc.stdout.read()

            text = build_message(
                    rev,
                    node.find('author').text,
                    node.find('date').text,
                    node.find('msg').text,
                    diff_data)

            subject = '[%(sect)s: %(rev)s]' % locals()

            sendmail.send(
                    mail_data['fromaddr'],
                    opts.get('address'),
                    subject,
                    text,
                    smtpserver=mail_data['smtpserver'])

            conf.set(sect, 'newest_rev', rev)

    conf.write(open(config_file, 'wt'))

