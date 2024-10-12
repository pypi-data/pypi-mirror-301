import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Tambahkan path ke 'pages' ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))

from login_page import LoginPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def test_login(driver):
    login_page = LoginPage(driver)

    # Test login
    login_page.open_login_page()
    login_page.enter_email('zenweltesting@gmail.com')
    login_page.enter_password('zenweltesting')
    login_page.click_login()
    assert login_page.verify_login_success(), "Login gagal!"