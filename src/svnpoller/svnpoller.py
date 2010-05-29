import os, sys
from urlparse import urlparse, urlunparse
from ConfigParser import ConfigParser
import sendmail
from svnlog import *

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svnpoller.ini')

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


def main(config_file):
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
        logs = (get_log(base_url, rev) for rev in revs)

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


def run():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = CONFIG_PATH

    main(config_file)


if __name__ == '__main__':
    run()

