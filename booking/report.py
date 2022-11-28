from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

class ReportBooking():
    def __init__(self, result_boxes:WebElement, driver:WebDriver):
        self.driver = driver
        self.report_boxes = result_boxes
        self.deal_boxes = self.pull_deal_box()
        self.airlines = []
        self.depart_date = []
        self.flight_time = []
        self.arrival_date = []

    def pull_deal_box(self):
        return self.report_boxes.find_elements_by_class_name(
                    'css-17f6u3r-searchResultsList'
                )

    def pull_flight_info_draft(self):
        for deal_box in self.deal_boxes:
            airlines = deal_box.find_elements_by_class_name(
                'Text-module__root--variant-small_1___16UY4'
            )
            self.depart_date.append(airlines[2].get_attribute('innerHTML'))
            self.flight_time.append(airlines[3].get_attribute('innerHTML'))
            self.arrival_date.append(airlines[6].get_attribute('innerHTML'))
            if len(airlines) > 10:
                self.airlines.append(
                    airlines[10].get_attribute('innerHTML').strip()+'|'+
                    airlines[8].get_attribute('innerHTML').strip())
            else:
                self.airlines.append(airlines[8].get_attribute('innerHTML').strip())
            time.sleep(0.5)
        print(self.airlines)
    
    def pull_flight_info(self):
        for deal_box in self.deal_boxes:
            see_flight_button = self.driver.find_element_by_css_selector(
                'button[data-testid="flight_card_bound_select_flight"]'
            )
            see_flight_button.click()
            time.sleep(0.5)
            info = deal_box.find_elements_by_class_name(
                'Text-module__root--variant-small_1___16UY4'
            )
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ESCAPE)
            actions.perform()
            time.sleep(0.1)
        for i in info:
            print(i.get_attribute('innerHTML'))