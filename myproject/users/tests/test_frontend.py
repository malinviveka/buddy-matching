from django.test import LiveServerTestCase
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class AccountCreationUITest(LiveServerTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Makes the test run in the background
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=chrome_options) 


    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_user_can_fill_out_form(self):
        """Test if a user can fill out and submit the account creation form"""
        self.browser.get(self.live_server_url + '/create-account/')  

    
        self.browser.find_element(By.ID, "id_first_name").send_keys("John")
        self.browser.find_element(By.NAME, "surname").send_keys("Doe")
        self.browser.find_element(By.NAME, "app_matr_number").send_keys("123456")
        self.browser.find_element(By.NAME, "email").send_keys("test@example.com")
        self.browser.find_element(By.NAME, "password1").send_keys("SecurePass123")
        self.browser.find_element(By.NAME, "password2").send_keys("SecurePass123")

        country_select = Select(self.browser.find_element(By.NAME, "country"))
        country_select.select_by_visible_text("Ghana")
        

        self.browser.find_element(By.ID, "submitAccountButton").click()
        time.sleep(1)  # Wait till site is loaded

        # check if account creation seems to have worked (from ui perspective)
        self.assertIn("Account created successfully!", self.browser.page_source)
