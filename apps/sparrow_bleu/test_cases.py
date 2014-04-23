from django.test import LiveServerTestCase
from nose.plugins.attrib import attr
from selenium.webdriver.firefox.webdriver import WebDriver


@attr(e2e=True)
class E2ETestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        # Implicitly wait means if we don't find an element automatically keep looking for 10 seconds
        cls.driver.implicitly_wait(10)
        super(E2ETestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(E2ETestCase, cls).tearDownClass()
        cls.driver.quit()

    def get_remote(self, url):
        self.driver.get(url)

    def get_local(self, url):
        '''
        Automatically puts WebDriver url in front

        Example:
            self.get_local(reverse('home'))
        '''
        self.driver.get("%s%s" % (self.live_server_url, url))
