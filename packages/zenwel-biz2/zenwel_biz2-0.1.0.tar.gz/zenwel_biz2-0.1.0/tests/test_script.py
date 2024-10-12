import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Tambahkan path ke 'pages' ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))

from login_page import LoginPage
from location_page import LocationPage

@pytest.fixture
def driver():
    # Setup WebDriver fixture for Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)  # Set implicit wait for better stability
    yield driver
    driver.quit()

def test_login_and_select_location(driver):
    # Test login functionality and location selection
    login_page = LoginPage(driver)
    location_page = LocationPage(driver)

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