from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging

class ForgotPage:
    def __init__(self, driver):
        self.driver = driver

    def open_login_page(self):
        logging.info("Membuka halaman login")
        self.driver.get("https://dashboard.zenwel.com")

    def click_forgot_password(self):
        logging.info("Mengklik tombol 'Forgot Password'")
        forgot_password_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.el-button.font-14.font-bold.color-blue.txt-align-lt.el-button--text"))
        )
        forgot_password_button.click()

    def enter_reset_email(self, email):
        logging.info("Memastikan popup 'Reset Password' terlihat")
        reset_password_popup = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.el-dialog__body"))
        )

        logging.info("Memasukkan email untuk reset password")
        email_input = reset_password_popup.find_element(By.CSS_SELECTOR, "input[type='email']")
        email_input.send_keys(email)

        logging.info("Mengklik tombol submit")
        submit_button = reset_password_popup.find_element(By.CSS_SELECTOR, "button[type='button']")
        submit_button.click()

    def set_new_password(self, new_password):
        logging.info("Memasukkan password baru")
        new_password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        new_password_input.send_keys(new_password)
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='button']"))
        )
        submit_button.click()

    def verify_reset_success(self):
        logging.info("Memverifikasi apakah dashboard telah dimuat")
        try:
            dashboard_image = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[@alt='Zenwel Dashboard']"))
            )
            logging.info("Dashboard berhasil dimuat")
            return True
        except Exception as e:
            logging.error("Dashboard tidak dimuat", exc_info=True)
            return False