import unittest, os

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

def command(cmd):
    #if 'dummy-url' not in cmd:
    #    return command_orig(cmd)

    if 'info' in cmd:
        return open(os.path.join(FIXTURE_DIR, 'info-1.xml')).read(), ''
    elif 'log' in cmd:
        return open(os.path.join(FIXTURE_DIR, 'log-1v.xml')).read(), ''
    elif 'diff' in cmd:
        return open(os.path.join(FIXTURE_DIR, 'diff-1.txt')).read(), ''
    else:
        return command_orig(cmd)

from svnpoller import svnlog
command_orig = svnlog.command


class TestBase(unittest.TestCase):

    def _stub_sendmail(self, fromaddr, toaddrs, msg, smtpserver):
        self._sent.append(locals())

    def setUp(self):
        from svnpoller import sendmail
        self.sendmail_orig = sendmail._sendmail

        self._sent = []
        sendmail._sendmail = self._stub_sendmail

        svnlog.command = command

    def tearDown(self):
        from svnpoller import sendmail
        sendmail._sendmail = self.sendmail_orig

        svnlog.command = command_orig


