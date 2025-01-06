import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


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
    Check_blanket = (By.XPATH, '/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    Add_icecream = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    Icecream_amount = (By.CLASS_NAME, 'counter-value')
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
        return self.driver.find_element(*self.Full_phone_number).get_attribute('text')

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
        return self.driver.find_element(*self.Check_blanket).is_selected()

    def click_add_icecream(self):
        self.driver.find_element(*self.Add_icecream).click()

    def get_icecream_amount(self):
        return self.driver.find_element(*self.Icecream_amount).get_property('value')

    def click_hail_cab(self):
        self.driver.find_element(*self.Button_hail_cab).click()

    def get_search_cab_modal(self):
        return self.driver.find_element(*self.Search_cab_modal).is_displayed()

    def get_driver_rating(self):
        WebDriverWait(self.driver, 40).until(expected_conditions.visibility_of_element_located(self.Driver_rating))
        self.driver.find_element(*self.Driver_rating).click()
        return self.driver.find_element(*self.Driver_rating).is_displayed()


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("perfLoggingPrefs", {'enableNetwork': True, 'enablePage': True})
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)
        self.routes_page.click_fare_details()
        self.routes_page.click_comfort_tariff()
        assert self.routes_page.get_comfort_is_selected()

    def test_fill_phone_number_modal(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)
        self.routes_page.click_fare_details()
        self.routes_page.click_comfort_tariff()
        self.routes_page.click_open_phone_number_modal()
        self.routes_page.fill_phone_modal(data.phone_number)
        assert self.routes_page.get_phone_number() == data.phone_number

    def test_fill_credit_card_modal(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        number = data.card_number
        code = data.card_code
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)
        self.routes_page.click_fare_details()
        self.routes_page.click_comfort_tariff()
        self.routes_page.fill_payment_method(number, code)
        assert self.routes_page.get_card_number() == number
        assert self.routes_page.get_card_code() == code
        self.routes_page.exit_payment_method()

    def test_message_for_driver(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        message = data.message_for_driver
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)
        self.routes_page.click_fare_details()
        self.routes_page.click_comfort_tariff()
        self.routes_page.input_driver_message(message)
        assert self.routes_page.get_driver_message() == message

    def test_ask_for_blanket_an_tissues(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)
        self.routes_page.click_fare_details()
        self.routes_page.click_comfort_tariff()
        self.routes_page.click_blanket_and_tissues()
        sleep(2)
        assert self.routes_page.get_blanket_and_tissues()

    def test_add_icecream(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)
        self.routes_page.click_fare_details()
        self.routes_page.click_comfort_tariff()
        self.routes_page.click_add_icecream()
        self.routes_page.click_add_icecream()
        assert self.routes_page.get_icecream_amount() == 2

    def test_search_cab_modal(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        number = data.card_number
        code = data.card_code
        message = data.message_for_driver
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)
        self.routes_page.click_fare_details()
        self.routes_page.click_comfort_tariff()
        self.routes_page.click_open_phone_number_modal()
        self.routes_page.fill_phone_modal(data.phone_number)
        self.routes_page.fill_payment_method(number, code)
        self.routes_page.exit_payment_method()
        self.routes_page.input_driver_message(message)
        self.routes_page.click_blanket_and_tissues()
        self.routes_page.click_add_icecream()
        self.routes_page.click_add_icecream()
        self.routes_page.click_hail_cab()
        sleep(2)
        assert self.routes_page.get_search_cab_modal()

    def test_fare_details(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        number = data.card_number
        code = data.card_code
        message = data.message_for_driver
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)
        self.routes_page.click_fare_details()
        self.routes_page.click_comfort_tariff()
        self.routes_page.click_open_phone_number_modal()
        self.routes_page.fill_phone_modal(data.phone_number)
        self.routes_page.fill_payment_method(number, code)
        self.routes_page.exit_payment_method()
        self.routes_page.input_driver_message(message)
        self.routes_page.click_blanket_and_tissues()
        self.routes_page.click_add_icecream()
        self.routes_page.click_add_icecream()
        self.routes_page.click_hail_cab()
        assert self.routes_page.get_driver_rating()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
