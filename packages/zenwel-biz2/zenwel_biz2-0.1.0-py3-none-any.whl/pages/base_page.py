import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def find_element(self, *locator, timeout=None):
        actual_timeout = timeout if timeout else self.timeout
        try:
            self.logger.info(f"Menunggu elemen dengan locator: {locator}")
            element = WebDriverWait(self.driver, actual_timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.info(f"Elemen ditemukan: {locator}")
            return element
        except Exception as e:
            self.logger.error(f"Gagal menemukan elemen dengan locator: {locator} - {e}")
            raise

    def click(self, *locator, timeout=None):
        try:
            element = self.find_element(*locator, timeout=timeout)
            element.click()
            self.logger.info(f"Berhasil mengklik elemen: {locator}")
        except Exception as e:
            self.logger.error(f"Gagal mengklik elemen dengan locator: {locator} - {e}")
            raise

    def enter_text(self, text, *locator, timeout=None):
        try:
            element = self.find_element(*locator, timeout=timeout)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Berhasil memasukkan teks '{text}' ke elemen: {locator}")
        except Exception as e:
            self.logger.error(f"Gagal memasukkan teks ke elemen dengan locator: {locator} - {e}")
            raise