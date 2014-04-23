from django_selenium.livetestcases import SeleniumLiveTestCase


class BasicTest(SeleniumLiveTestCase):

    def test_index(self):
        resp = self.driver.open_url("http://localhost:8000")

        self.assertEquals(True, False)
