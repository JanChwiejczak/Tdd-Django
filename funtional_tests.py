from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self):
        # Peter is going to check out our to-do app.
        # He goes to its homepage
        self.browser.get('http://127.0.0.1:8000/')

        # He noticed the page title and header mention to-do list
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # He is invited to enter a to-do item straight away

        # He types "Buy tickets to Stockholm" into a text box.

        # When he hits Enter, the page updates and now the list shows:
        # "1. Buy tickets to Stockholm" as an item on to-do list

        # There still is a text box inviting him to add another item.
        # He types "Book a hotel for upcoming trip to Sweden".

        # The page updates and now he sees both items on his list.

        # Peter wonders whether the site will remember his list. Then he
        # sees that the site generated a unique URL for him - there is
        # explanatory text to that effect.

        # He visits that URL - the entered tasks are still there.

        # Satisfied he goes to sleep.
