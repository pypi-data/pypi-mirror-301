import time
import pytest
import logging
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def open_login_page(self):
        pass

    def enter_email(self, email):
        email_input = self.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@resource-id='email_input_id']")
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = self.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@resource-id='password_input_id']")
        password_input.send_keys(password)

    def click_login(self):
        login_button = self.driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@resource-id='login_button_id']")
        login_button.click()

    def verify_login_success(self):
        time.sleep(4)
        try:
            location_text = self.driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Pilih lokasi transaksi')]")
            return True
        except:
            return False

@pytest.fixture(scope="module")
def driver():
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "13.0",  # Ganti dengan versi Android yang sesuai dengan emulator Anda
        "deviceName": "Android",  # Sesuaikan dengan nama AVD Anda
        "appPackage": "com.zenwel.biz",  # Ganti dengan package name aplikasi Anda
        "appActivity": "com.zenwel.biz.MainActivity",  # Ganti dengan activity utama aplikasi Anda
        "automationName": "UiAutomator2"
    }
    logging.info(f"Desired Capabilities: {desired_caps}")
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    yield driver
    driver.quit()

def test_login(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.enter_email("test@example.com")
    login_page.enter_password("password123")
    login_page.click_login()
    assert login_page.verify_login_success() == True