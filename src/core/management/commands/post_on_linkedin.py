
from django.core.management.base import BaseCommand
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

import os

class Command(BaseCommand):
    help = 'Opens a web page specified by settings.LINKEDIN_URL using Selenium'

    def handle(self, *args, **options):
        url = getattr(settings, 'LINKEDIN_URL', None)
        TEST_MODE = getattr(settings, 'TEST_MODE', False)
        if not url:
            self.stderr.write(self.style.ERROR("LINKEDIN_URL is not defined in settings.py"))
            return

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.binary_location = os.environ.get('CHROMIUM_BIN', '/usr/bin/chromium')

        service = Service(executable_path=os.environ.get('CHROMEDRIVER_BIN', '/usr/bin/chromedriver'))

        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            self.stdout.write(self.style.SUCCESS("Launching Chromium/Google Chrome in headless mode..."))

            driver.get(url)
            if TEST_MODE:
                driver.save_screenshot('screenshot.png')
            self.stdout.write(self.style.SUCCESS(f"Successfully opened URL: {url}"))
            self.stdout.write(self.style.SUCCESS(f"Page Title: {driver.title}"))

        except WebDriverException as e:
            self.stderr.write(self.style.ERROR(f"WebDriverException occurred: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Exception occurred: {e}"))
        finally:
            if 'driver' in locals():
                driver.quit()
                self.stdout.write(self.style.SUCCESS("Closed the browser successfully."))
