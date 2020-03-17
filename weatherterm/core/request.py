from selenium import webdriver
import os


class Request:

    def __init__(self, base_url):
        self._base_url = base_url
        # we find the phantomjs path which is in the phantomjs directory by using os.path.join to
        # join the current directory with the phantomjs executable
        self._phantomjs_path = os.path.join(os.curdir, 'phantomjs/bin/phatmomjs')
        # PhantomJS of selenium is then run using the phantomjs directory path
        self._driver = webdriver.PhantomJS(self._phantomjs_path)

    def fetch_data(self, area, forecast):
        """Fetching the data for weather from the site using the area code"""
        url = self._base_url.format(forecast=forecast, area=area)
        self._driver.get(url)

        # if url does not exist or data not available raise custom error message
        # this is because selenium does not produce status codes so we just have to compare strings
        if self._driver == '404 Not Found':
            error_message = 'Could not find the area you were searching for'
            raise Exception(error_message)
        # if everything runs smoothly, return the page source
        return self._driver.page_source
