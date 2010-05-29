import os
from tempfile import mkstemp
from ConfigParser import ConfigParser

import base
from svnpoller import svnpoller

TEST_URL = 'http://svn.plone.org/svn/collective/PloneTranslations/trunk/i18n/atcontenttypes-ja.po'
TEST_REVS = [106448, 107126, 113304, 113533, 114575, 115025]

CONFIG_DATA = '''\
[mail]
smtpserver = localhost
fromaddr = poller@example.com

[PloneTranslations-ja]
url = http://svn.plone.org/svn/collective/PloneTranslations/trunk/i18n/atcontenttypes-ja.po
newest_rev = 1
address = user1@example.com
'''

class TestSvnPoller(base.TestBase):

    def setUp(self):
        super(TestSvnPoller, self).setUp()
        h,fname = mkstemp()
        os.write(h, CONFIG_DATA)
        os.close(h)
        self.config_file = fname

    def tearDown(self):
        if os.path.exists(self.config_file):
            os.unlink(self.config_file)
        super(TestSvnPoller, self).tearDown()

    def test_mail_payload(self):
        svnpoller.main(self.config_file, self._stub_sender)

        self.assertEqual(len(TEST_REVS), len(self._sent))
        self.assertEqual('poller@example.com', self._sent[0]['fromaddr'])
        self.assertEqual(('user1@example.com',), self._sent[0]['toaddrs'])
        self.assertEqual('localhost', self._sent[0]['smtpserver'])

    def test_config_update(self):
        svnpoller.main(self.config_file, self._stub_sender)

        conf = ConfigParser()
        conf.read(self.config_file)
        self.assertEqual(str(TEST_REVS[-1]),
                         conf.get('PloneTranslations-ja', 'newest_rev'))


