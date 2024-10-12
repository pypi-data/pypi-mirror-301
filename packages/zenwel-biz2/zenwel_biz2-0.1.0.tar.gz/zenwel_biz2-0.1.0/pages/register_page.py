# register_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class RegisterPage:
    def __init__(self, driver):
        self.driver = driver

    def click_register_link(self):
        logging.info("Mengklik tautan 'Mulailah secara gratis'")
        register_link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.color-blue.font-14.font-bold.word-break"))
        )
        register_link.click()

    def fill_personal_details(self, name, email, phone, password):
        logging.info("Mengisi formulir pendaftaran person")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        ).send_keys(name)
        
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.CSS_SELECTOR, "input.el-input__inner[type='tel']").send_keys(phone)
        self.driver.find_element(By.NAME, "password").send_keys(password)

       # Verifikasi CAPTCHA
        logging.info("Menangani verifikasi CAPTCHA")
        captcha_frame = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
        )
        self.driver.switch_to.frame(captcha_frame)
        self.driver.find_element(By.XPATH, "//div[@class='recaptcha-checkbox-border']").click()
        self.driver.switch_to.default_content()
        
        # Tunggu input dari pengguna untuk konfirmasi CAPTCHA selesai
        input("Silakan selesaikan CAPTCHA dan tekan Enter jika sudah selesai...")
        
        # Klik tombol submit
        logging.info("Mengklik tombol 'Lanjutkan'")
        lanjutkan_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.el-button.el-button--primary"))
        )
        lanjutkan_button.click()

    def verify_otp(self):
        logging.info("Menunggu input OTP dari pengguna")
        otp_code = input("Masukkan kode OTP yang diterima melalui SMS: ")
        
        otp_input_fields = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.el-input__inner[type='number']"))
        )
        
        for i, digit in enumerate(otp_code):
            otp_input_fields[i].send_keys(digit)

        logging.info("Kode OTP berhasil dimasukkan")

    def fill_business_details(self, business_name, business_type, country, timezone, address, city):
        logging.info("Mengisi formulir pendaftaran bisnis")

        # Isi Nama Perusahaan
        self.driver.find_element(By.NAME, "company_name").send_keys(business_name)

        # Isi Tipe Bisnis
        logging.info("Selecting 'Tipe Bisnis' from dropdown")
        business_type_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.el-select"))
        )
        business_type_dropdown.click()
        
        business_type_option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{business_type}']"))
        )
        business_type_option.click()

         # Hentikan sementara pengujian dan tunggu input dari terminal
        input("Pengujian dihentikan sementara. Tekan Enter untuk melanjutkan...")

        #self.driver.find_element(By.NAME, "country").send_keys(country)
        #self.driver.find_element(By.NAME, "timezone").send_keys(timezone)
        self.driver.find_element(By.NAME, "address").send_keys(address)

        logging.info("Selecting 'City' from dropdown")
        city_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.multiselect__tags"))
        )
        city_dropdown.click()
        
        city_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Masukkan kata kunci']"))
        )
        city_input.send_keys(city)
        
        city_option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{city}']"))
        )
        city_option.click()
        
        self.driver.find_element(By.CSS_SELECTOR, "button[type='button']").click()
        
        #self.driver.find_element(By.CSS_SELECTOR, "button[type='button']").click()


    def verify_account_creation(self):
        logging.info("Memverifikasi bahwa akun berhasil dibuat")
        try:
            success_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Welcome')]"))
            )
            return True
        except Exception as e:
            logging.error("Akun tidak berhasil dibuat", exc_info=True)
            return False