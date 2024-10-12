# test_register.py
import sys
import os
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Tambahkan path ke 'pages' ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))

from register_page import RegisterPage

logging.basicConfig(level=logging.INFO)

@pytest.fixture
def driver():
    # Setup WebDriver fixture for Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)  # Set implicit wait for better stability
    yield driver
    driver.quit()

def test_register_flow(driver):
    register_page = RegisterPage(driver)
    
    try:
        # Buka halaman login
        logging.info("Membuka halaman login")
        driver.get("https://dashboard.zenwel.com")
        
        # Klik tautan "Mulailah secara gratis"
        register_page.click_register_link()
        
        # Isi formulir pendaftaran person
        register_page.fill_personal_details("John Doe", "budisumiarsih.zenwel@gmail.com", "+6285294229442", "zenwel")
        
        # Verifikasi OTP
        register_page.verify_otp()
        
        # Isi formulir pendaftaran bisnis
        register_page.fill_business_details("Martha Tilaar", "Yoga Studio", "Indonesia", "Indonesia (GMT +7)", "Jl Mataram Timur Raya No 4, Sumberadi Mlati Sleman D.I Yogyakarta", "Sleman")
        
        # Verifikasi bahwa akun berhasil dibuat
        assert register_page.verify_account_creation(), "Pembuatan akun gagal!"
        logging.info("Pembuatan akun berhasil")
        
    except Exception as e:
        driver.save_screenshot(os.path.join(os.getcwd(), "screenshot.png"))
        logging.error("Terjadi kesalahan, screenshot diambil.", exc_info=True)
        raise e