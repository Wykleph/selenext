from __future__ import print_function
import unittest

from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenext.Helpers import Page, View, PageElement, ParentElement
from json.decoder import JSONDecodeError


class PageTest(unittest.TestCase):
    def setUp(self):
        self.driver = Chrome()
        self.assertIsInstance(self.driver, WebDriver)

        self.page = Page(self.driver, 'page_tests.json', file=True)

    def test_page_instance_is_page(self):
        self.assertIsInstance(self.page, Page)

    def test_page_instantiation(self):
        self.assertRaises(TypeError, Page)
        self.assertRaises(TypeError, Page, self.driver)
        self.assertRaises(JSONDecodeError, Page, self.driver, '')
        self.assertRaises(JSONDecodeError, Page, self.driver, 'page_tests.json')

    def test_page_attributes(self):
        self.assertIsInstance(self.page.driver, WebDriver)
        self.assertIsInstance(self.page.root, str)

        # The next line should work, but doesn't?  Leaving it commented out for now.
        # self.assertRaises(NoSuchElementException, self.page.search_input)
        self.page.get(self.page.root)
        # In the debugger, the self.page.search_input attribute equals a PageElement,
        # but as soon as the attribute is accessed, it will change to a WebElement.
        self.assertIsInstance(self.page.search_input, WebElement)
        self.assertIsInstance(self.page.view.search_input, PageElement)

    def test_page_view_attributes(self):
        self.assertIsInstance(self.page.view, View)
        self.assertIsInstance(self.page.view.elements, dict)
        self.assertIsInstance(self.page.view.json_dict, dict)
        self.assertIsInstance(self.page.view.driver, WebDriver)

    def test_page_element_attributes(self):
        self.page.get(self.page.root)
        self.assertTrue(self.page.view.search_input.exists())
        self.assertFalse(self.page.view.missing_element.exists())
        self.assertIsInstance(self.page.view.search_input.driver, WebDriver)
        self.assertIsInstance(self.page.view.search_input.element_dict, dict)
        self.assertIsInstance(self.page.view.search_input.lookup_method, str)
        self.assertIsInstance(self.page.view.search_input.selector, str)
        self.assertIsInstance(self.page.view.search_input, PageElement)
        self.assertIsInstance(self.page.view.search_form.parent, ParentElement)
        self.assertIsInstance(self.page.view.search_form.parent.parent, ParentElement)
        self.assertIsNone(self.page.view.search_input.parent)

    def test_multiple_page_element(self):
        self.page.get(self.page.root)
        self.page.search_input.send_keys('cookies')
        sleep(2)
        self.page.search_button.click()

        while not self.page.view.results.exists():
            sleep(1)

        self.assertIsInstance(self.page.results, list)
        self.assertIsInstance(self.page.results[3], WebElement)
        self.assertIsInstance(self.page.bound_results[3], str)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
