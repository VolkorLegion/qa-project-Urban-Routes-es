import data
from selenium import webdriver
from time import sleep
from pages import UrbanRoutesPage


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
        self.test_set_route()
        self.routes_page.click_fare_details()
        self.routes_page.click_comfort_tariff()
        assert self.routes_page.get_comfort_is_selected()

    def test_fill_phone_number_modal(self):
        self.test_select_comfort_tariff()
        self.routes_page.click_open_phone_number_modal()
        self.routes_page.fill_phone_modal(data.phone_number)
        assert self.routes_page.get_phone_number()

    def test_fill_credit_card_modal(self):
        self.test_fill_phone_number_modal()
        number = data.card_number
        code = data.card_code
        self.routes_page.fill_payment_method(number, code)
        assert self.routes_page.get_card_number() == number
        assert self.routes_page.get_card_code() == code
        self.routes_page.exit_payment_method()

    def test_message_for_driver(self):
        self.test_fill_credit_card_modal()
        message = data.message_for_driver
        self.routes_page.input_driver_message(message)
        assert self.routes_page.get_driver_message() == message

    def test_ask_for_blanket_an_tissues(self):
        self.test_message_for_driver()
        self.routes_page.click_blanket_and_tissues()
        sleep(2)
        assert self.routes_page.get_blanket_and_tissues()

    def test_add_icecream(self):
        self.test_ask_for_blanket_an_tissues()
        self.routes_page.click_add_icecream()
        self.routes_page.click_add_icecream()
        assert self.routes_page.get_icecream_amount()

    def test_search_cab_modal(self):
        self.test_add_icecream()
        self.routes_page.click_hail_cab()
        sleep(2)
        assert self.routes_page.get_search_cab_modal()

    def test_driver_details(self):
        self.test_search_cab_modal()
        assert self.routes_page.get_driver_rating()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
