from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LocationPage:
    def __init__(self, driver):
        self.driver = driver

    def select_location(self, location_name):
        # Select the specified location by name
        try:
            location_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'block-link flex-block-link pointer ml-auto mr-auto') and .//div[contains(text(),'{location_name}')]]"))
            )
            location_button.click()
            return True
        except Exception as e:
            print(f"Gagal memilih lokasi transaksi: {e}")
            return False

    def verify_dashboard_loaded(self):
        # Verify that the dashboard is loaded successfully
        try:
            dashboard_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//li[@id='menu-wrapper--home' and @class='el-menu-item is-active submenu-title-noDropdown']"))
            )
            return True
        except Exception as e:
            print(f"Gagal memuat beranda: {e}")
            return False