from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import booking.constant as const
import datetime as dt
import time
from booking.booking_filter import Filter
from booking.report import ReportBooking


class Booking(webdriver.Chrome):
    def __init__(self, quit_browser=False):
        super().__init__(executable_path='driver/chromedriver')
        self.implicitly_wait(8)
        self.teardown = quit_browser

    def __exit__(self, *args):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.find_element(
            by=By.CSS_SELECTOR,
            value='span.bui-button__text'
        )
        currency_element.click()
        selected_currency = self.find_element(
            by=By.CSS_SELECTOR,
            value=f'a[data-modal-header-async-url-param*="changed_currency=1;selected_currency={currency}"]'
        )
        selected_currency.click()

    def search_airport(self, flight_origin, flight_destination):

        ###### Origin ######
        flight_button = self.find_element(
            by=By.CSS_SELECTOR,
            value='a[data-decider-header="flights"]'
        )
        flight_button.click()

        one_way_button = self.find_element(
            by=By.CSS_SELECTOR,
            value='div[data-testid="searchbox_controller_trip_type_ONEWAY"]'
        )
        one_way_button.click()

        from_bar = self.find_element(
            by=By.CSS_SELECTOR,
            value='div[data-testid="searchbox_origin"]'
        )
        from_bar.click()

        from_input = self.find_element(
            by=By.CSS_SELECTOR,
            value='input[data-testid="searchbox_origin_input"]'
        )
        from_input.send_keys(Keys.BACK_SPACE)
        from_input.send_keys(flight_origin)

        first_airport = self.find_element(
            by=By.CSS_SELECTOR,
            value='div[data-testid="autocomplete_result"]'
        )
        first_airport.click()

        time.sleep(3)

        ###### Destination ######
        destination_input = self.find_element(
            by=By.CSS_SELECTOR,
            value='input[data-testid="searchbox_destination_input"]'
        )
        destination_input.send_keys(Keys.BACK_SPACE)
        destination_input.send_keys(flight_destination)

        first_airport = self.find_element(
            by=By.CSS_SELECTOR,
            value='div[data-testid="autocomplete_result"]'
        )
        first_airport.click()

    def search_date(self, flight_date):
        selected_date_bar = self.find_element_by_css_selector(
            'input[placeholder="Depart"]'
        )
        selected_date_bar.click()

        selected_month = int(flight_date.split('-')[1])
        current_month = int(dt.datetime.today().month)
        click_time = selected_month - current_month - 1
        if click_time < 0:
            click_time = 0
        next_month = self.find_element_by_css_selector(
            'button[class="Calendar-module__control___2XUQu Calendar-module__control--next___1iU98"]'
        )
        i = 0
        while i < click_time:
            next_month.click()
            i += 1

        selected_date = self.find_element_by_css_selector(
            f'span[data-date-cell="{flight_date}"]'
        )
        selected_date.click()

    def click_search(self):
        search_button = self.find_element_by_css_selector(
            'button[data-testid="searchbox_submit"]'
        )
        search_button.click()

    def filter(self):
        filtration = Filter(driver=self)

        # 12:00 AM - 5:59 AM == 1
        # 6:00 AM - 11:59 AM == 2
        # 12:00 PM - 5:59 PM == 3
        # 6:00 PM - 11:59 PM == 4
        filtration.filter_depart_time(2, 3)

    def report_result(self):
        result_boxes = self.find_element_by_class_name(
            'css-1mxydpm'
        )
        report = ReportBooking(result_boxes=result_boxes, driver=self)
        report.pull_flight_info_draft()
        # report.pull_flight_info()
