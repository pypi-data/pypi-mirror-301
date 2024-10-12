import sys
import os
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Tambahkan path ke 'pages' ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))

from forgot_page import ForgotPage

logging.basicConfig(level=logging.INFO)

@pytest.fixture
def driver():
    # Setup WebDriver fixture for Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)  # Set implicit wait for better stability
    yield driver
    driver.quit()

def test_forgot_password_flow(driver):
    login_page = ForgotPage(driver)
    
    try:
        # Buka halaman login
        logging.info("Membuka halaman login")
        login_page.open_login_page()
        
        # Klik link "Forgot Password"
        logging.info("Mengklik link 'Forgot Password'")
        login_page.click_forgot_password()
        
        # Masukkan email untuk reset password
        logging.info("Memasukkan email untuk reset password")
        login_page.enter_reset_email("zenweltesting@gmail.com")
        
        # Tunggu email masuk dan minta input link dari terminal
        reset_link = input("Masukkan link reset password dari email: ")
        logging.info(f"Menggunakan link reset password: {reset_link}")
        driver.get(reset_link)
        
        # Set password baru
        logging.info("Mengatur password baru")
        login_page.set_new_password("zenweltesting")
        
        # Verifikasi reset password berhasil
        assert login_page.verify_reset_success(), "Reset password gagal!"
        logging.info("Reset password berhasil")
        
    except Exception as e:
        driver.save_screenshot(os.path.join(os.getcwd(), "screenshot.png"))
        logging.error("Terjadi kesalahan, screenshot diambil.", exc_info=True)
        raise e