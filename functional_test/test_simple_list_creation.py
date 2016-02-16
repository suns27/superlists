from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class newVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('buy something')

        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1:buy something')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy another')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1:buy something')
        self.check_for_row_in_list_table('2:buy another')

        self.browser.quit()
        self.browser = webdriver.Chrome(executable_path='c:\python34\chromedriver.exe')

        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy something', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy milk')
        inputbox.send_keys(Keys.ENTER)

        francis_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy something', page_text)
        self.assertIn('buy milk', page_text)
        
        self.fail('finish')
