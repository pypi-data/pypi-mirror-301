# test_script.py
import sys
import os
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Tambahkan path ke 'pages' ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))

from login_page import LoginPage
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
    forgot_page = ForgotPage(driver)
    
    try:
        # Buka halaman login
        logging.info("Membuka halaman login")
        forgot_page.open_login_page()
        
        # Klik link "Forgot Password"
        logging.info("Mengklik link 'Forgot Password'")
        forgot_page.click_forgot_password()
        
        # Masukkan email untuk reset password
        logging.info("Memasukkan email untuk reset password")
        forgot_page.enter_reset_email("zenweltesting@gmail.com")
        
        # Tunggu email masuk dan minta input link dari terminal
        reset_link = input("Masukkan link reset password yang Anda terima di email: ")
        logging.info(f"Menggunakan link reset password: {reset_link}")
        driver.get(reset_link)
        
        # Set password baru
        logging.info("Mengatur password baru")
        forgot_page.set_new_password("zenweltesting")
        
        # Verifikasi reset password berhasil
        assert forgot_page.verify_reset_success(), "Reset password gagal!"
        logging.info("Reset password berhasil")
        
    except Exception as e:
        driver.save_screenshot(os.path.join(os.getcwd(), "screenshot.png"))
        logging.error("Terjadi kesalahan, screenshot diambil.", exc_info=True)
        raise e

def test_login_flow(driver):
    login_page = LoginPage(driver)
    
    try:
         # Test login
        print("Memulai pengujian login...")
        login_page.open_login_page()
        login_page.enter_email('zenweltesting@gmail.com')
        login_page.enter_password('zenweltesting')
        login_page.click_login()
        assert login_page.verify_login_success(), "Login gagal!"

        # Test pilih lokasi
        location_name = 'ZenDev - Accounting'
        print(f"Mencoba memilih lokasi: {location_name}")
        assert location_page.select_location(location_name), f"Gagal memilih lokasi transaksi: {location_name}"
        assert location_page.verify_dashboard_loaded(), "Gagal memuat beranda!"
        
    except Exception as e:
        driver.save_screenshot(os.path.join(os.getcwd(), "screenshot.png"))
        logging.error("Terjadi kesalahan, screenshot diambil.", exc_info=True)
        raise e