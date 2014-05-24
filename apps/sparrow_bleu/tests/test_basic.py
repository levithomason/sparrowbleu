from django.core.urlresolvers import reverse

from sparrow_bleu.test_cases import E2ETestCase


class BasicTest(E2ETestCase):

    def test_index(self):
        self.get_local(reverse('home'))

        self.assertIn('client-access', self.driver.current_url)

        brand_logo = self.driver.find_element_by_id('brand_sparrow_bleu')
        self.assertTrue(brand_logo)
