import os
import base
from svnpoller import svnlog

TEST_URL = 'http://svn.plone.org/svn/collective/PloneTranslations/trunk/i18n/atcontenttypes-ja.po'
TEST_REVS = [106448, 107126, 113304, 113533, 114575, 115025]


class TestSvnlog(base.TestBase):

    def setUp(self):
        super(TestSvnlog, self).setUp()

    def test_log_class(self):
        log = svnlog.Log(TEST_URL, TEST_REVS[0])
        self.assertEqual(TEST_REVS[0], log.rev)
        self.assertEqual(TEST_URL, log.url)
        self.assertEqual('http://svn.plone.org/svn/collective', log.root)
        self.assertEqual('/PloneTranslations/trunk/i18n/atcontenttypes-ja.po', log.subpath)
        self.assertEqual([('M', '/PloneTranslations/trunk/i18n/atcontenttypes-ja.po')], log.paths)
        #self.assertEqual('', log.normalized_paths)
        self.assertEqual('terapyon', log.author)
        self.assertEqual('2009-12-11 09:51:35', log.date.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('Japanse two portal message fixed #9922', log.msg)
        self.assert_(log.diff)

    def test_get_revisions_ids(self):
        revs = svnlog.get_revisions([TEST_URL])
        self.assertEqual(TEST_REVS, revs)

    def test_get_logs(self):
        logs = svnlog.get_logs(TEST_URL)
        self.assertEqual(6, len(logs))
        for log in logs:
            self.assert_(log.rev)
            self.assertEqual('http://svn.plone.org/svn/collective', log.root)

