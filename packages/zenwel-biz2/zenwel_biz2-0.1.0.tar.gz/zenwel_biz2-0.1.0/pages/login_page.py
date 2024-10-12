from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def open_login_page(self):
        # Open the login page
        self.driver.get("https://dashboard.zenwel.com")

    def enter_email(self, email):
        # Enter the email in the email input field
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_input.send_keys(email)

    def enter_password(self, password):
        # Enter the password in the password input field
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        password_input.send_keys(password)

    def click_login(self):
        # Click the login button
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button']"))
        )
        login_button.click()

    def verify_login_success(self):
        # Verify login success by checking for specific elements
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Pilih lokasi transaksi')]"))
            )
            return True
        except:
            return False