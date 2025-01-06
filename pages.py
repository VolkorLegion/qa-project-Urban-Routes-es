from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from helpers import retrieve_phone_code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    Button_ask_for_cab = (By.CLASS_NAME, 'button.round')
    Button_comfort_tariff = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]/div[1]/img')
    Button_phone_number = (By.CLASS_NAME, 'np-button')
    Full_phone_number = (By.CLASS_NAME, 'np-text')
    Phone_number_field = (By.ID, 'phone')
    Button_siguiente = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    SMS_code_input = (By.XPATH, '//*[@id="code"]')
    Button_confirmar = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    Button_payment = (By.CLASS_NAME, 'pp-text')
    Button_add_card = (By.CLASS_NAME, 'pp-plus-container')
    Add_card_number = (By.CLASS_NAME, 'card-input')
    Add_code = (By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/div[2]/div[2]/input')
    Confirm_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    Exit_payment = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    Card_is_selected = (By.CLASS_NAME, 'pp-value-text')
    Comment_input = (By.ID, 'comment')
    Check_blanket = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    Add_icecream = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    Icecream_amount = (By.CSS_SELECTOR, 'div.counter-value')
    Button_hail_cab = (By.CLASS_NAME, 'smart-button-main')
    Search_cab_modal = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[2]/div[1]/div[2]/button')
    Assert_comfort_tariff = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[1]')
    Driver_rating = (By.CLASS_NAME, 'order-btn-rating')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.to_field))
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_fare_details(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.Button_ask_for_cab))
        self.driver.find_element(*self.Button_ask_for_cab).click()

    def click_comfort_tariff(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.Button_comfort_tariff))
        self.driver.find_element(*self.Button_comfort_tariff).click()

    def get_comfort_is_selected(self):
        return self.driver.find_element(*self.Assert_comfort_tariff).is_displayed()

    def click_open_phone_number_modal(self):
        self.driver.find_element(*self.Button_phone_number).click()

    def fill_phone_modal(self, number_phone):
        self.driver.find_element(*self.Phone_number_field).send_keys(number_phone)
        self.driver.find_element(*self.Button_siguiente).click()
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.Assert_comfort_tariff))
        phone_code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.SMS_code_input).send_keys(phone_code)
        self.driver.find_element(*self.Button_confirmar).click()

    def get_phone_number(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.Full_phone_number))
        return self.driver.find_element(*self.Full_phone_number).is_displayed()

    def fill_payment_method(self, number_card, code_card):
        self.driver.find_element(*self.Button_payment).click()
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.Button_add_card))
        self.driver.find_element(*self.Button_add_card).click()
        self.driver.find_element(*self.Add_card_number).send_keys(number_card)
        self.driver.find_element(*self.Add_code).send_keys(code_card)
        self.driver.find_element(*self.Add_card_number).click()

    def get_card_number(self):
        return self.driver.find_element(*self.Add_card_number).get_property('value')

    def get_card_code(self):
        return self.driver.find_element(*self.Add_code).get_property('value')

    def exit_payment_method(self):
        self.driver.find_element(*self.Confirm_card).click()
        self.driver.find_element(*self.Exit_payment).click()

    def input_driver_message(self, cab_message):
        self.driver.find_element(*self.Comment_input).send_keys(cab_message)

    def get_driver_message(self):
        return self.driver.find_element(*self.Comment_input).get_property('value')

    def click_blanket_and_tissues(self):
        self.driver.find_element(*self.Check_blanket).click()

    def get_blanket_and_tissues(self):
        return self.driver.find_element(*self.Check_blanket).is_displayed()

    def click_add_icecream(self):
        self.driver.find_element(*self.Add_icecream).click()

    def get_icecream_amount(self):
        return self.driver.find_element(*self.Icecream_amount).is_displayed()

    def click_hail_cab(self):
        self.driver.find_element(*self.Button_hail_cab).click()

    def get_search_cab_modal(self):
        return self.driver.find_element(*self.Search_cab_modal).is_displayed()

    def get_driver_rating(self):
        WebDriverWait(self.driver, 40).until(expected_conditions.visibility_of_element_located(self.Driver_rating))
        self.driver.find_element(*self.Driver_rating).click()
        return self.driver.find_element(*self.Driver_rating).is_displayed()
