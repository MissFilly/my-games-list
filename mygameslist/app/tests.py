from selenium import webdriver
from django.test import LiveServerTestCase

class AdminTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_admin_site(self):
        # user opens web browser, navigates to admin page
        self.browser.get(self.live_server_url + '/admin/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)
