from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Peter is going to check out our to-do app.
        # He goes to its homepage
        self.browser.get('http://127.0.0.1:8000/')

        # He noticed the page title and header mention to-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Buy tickets to Stockholm" into a text box.
        inputbox.send_keys('Buy tickets to Stockholm')

        # When he hits Enter, the page updates and now the list shows:
        # "1. Buy tickets to Stockholm" as an item on to-do list
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1. Buy tickets to Stockholm')

        # There still is a text box inviting him to add another item.
        # He types "Book a hotel for upcoming trip to Sweden".
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Book a hotel for upcoming trip to Sweden')
        inputbox.send_keys(Keys.ENTER)

        # The page updates and now he sees both items on his list.
        self.check_for_row_in_list_table('1. Buy tickets to Stockholm')
        self.check_for_row_in_list_table('2. Book a hotel for upcoming trip to Sweden')

        # Peter wonders whether the site will remember his list. Then he
        # sees that the site generated a unique URL for him - there is
        # explanatory text to that effect.

        self.fail('Finish the test!')
        # He visits that URL - the entered tasks are still there.

        # Satisfied he goes to sleep.


