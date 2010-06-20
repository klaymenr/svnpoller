import unittest, os
from optparse import OptionParser
import minimock

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

svn_command_parser = OptionParser()
svn_command_parser.add_option('-r', '--revision',
                              action='store', type='string', dest='revision')
svn_command_parser.add_option('-c', '--change',
                              action='store', type='string', dest='change')
svn_command_parser.add_option('', '--xml',
                              action='store_true', default=False, dest='xml')
svn_command_parser.add_option('-v', '--verbose',
                              action='store', type='string', dest='verbose')
svn_command_parser.exit = lambda *args, **kw: None
svn_command_parser.error = lambda *args, **kw: None


def command(cmd):
    #if 'dummy-url' not in cmd:
    #    return command_orig(cmd)

    if 'info' == cmd[1]:
        return open(os.path.join(FIXTURE_DIR, 'info-1.xml')).read(), ''

    elif 'log' == cmd[1]:
        options, args = svn_command_parser.parse_args(cmd[2:])
        if options.change:
            rev = options.change
        elif options.revision:
            rev = options.revision.replace(':','-')
        else:
            rev = '1-HEAD'
        filename = 'log-%s.xml' % rev
        if not os.path.exists(os.path.join(FIXTURE_DIR, filename)):
            raise RuntimeError(filename+' was not found')

        f = os.path.join(FIXTURE_DIR, filename)
        #print f
        return open(f).read(), ''

    elif 'diff' == cmd[1]:
        f = os.path.join(FIXTURE_DIR, 'diff-1.txt')
        #print f
        return open(f).read(), ''

    else:
        raise RuntimeError("'%s' was not supported." % cmd)
        #return svnpoller.svnlog.command(cmd) # call original code.


class TestBase(unittest.TestCase):

    def _stub_sender(self, fromaddr, toaddrs, subject, message_text,
                     smtpserver='localhost', charset='utf-8', sender=None):

        def storage(fromaddr, toaddrs, msg, smtpserver):
            self._sent.append(locals())

        from svnpoller.sendmail import send
        send(fromaddr, toaddrs, subject, message_text,
             smtpserver=smtpserver, charset=charset, sender=storage)

    def setUp(self):
        self._sent = []
        import svnpoller.svnlog
        minimock.mock('svnpoller.svnlog.command', mock_obj=command)

    def tearDown(self):
        minimock.restore()


