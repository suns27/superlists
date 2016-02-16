from .base import FunctionalTest
from unittest import skip


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You cannot have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('buy milk')
        self.check_for_row_in_list_table('1:buy milk')

        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        self.check_for_row_in_list_table('1:buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You cannot have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('make tea')
        self.check_for_row_in_list_table('1:buy milk')
        self.check_for_row_in_list_table('2:make tea')
        self.fail('write me')
