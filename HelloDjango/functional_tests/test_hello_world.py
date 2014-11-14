from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import sys
import os
from datetime import datetime
import time

DEFAULT_WAIT = 5
SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                cls.against_staging = True
                return
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not cls.against_staging:
            super().tearDownClass()


    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return ('{folder}/{classname}.'
                '{method}-window{windowid}-{timestamp}').format(
                    folder=SCREEN_DUMP_LOCATION,
                    classname=self.__class__.__name__,
                    method=self._testMethodName,
                    windowid=self._windowid,
                    timestamp=timestamp
                )

    def wait_for(self, function_with_assertion, timeout=DEFAULT_WAIT):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)
        # one more try, which will raise any errors if they are outstanding
        return function_with_assertion()


class HelloWorldTest(FunctionalTest):

    def test_screen_prints_hello_world(self):
        # Billy goes to this great new site to see it say "Hello World"
        self.browser.get(self.server_url)

        # This awesome page prints "Hello World"... and that's it
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hello World!', page_text)
