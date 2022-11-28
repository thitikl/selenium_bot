from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class Filter():
    def __init__(self, driver:WebDriver) -> None:
        self.driver = driver
        self.time_dict = {
            1: '12:00 AM - 5:59 AM',
            2: '6:00 AM - 11:59 AM',
            3: '12:00 PM - 5:59 PM',
            4: '6:00 PM - 11:59 PM'
        }

    def filter_depart_time(self, *depart_time_keys):
        depart_time_box = self.driver.find_element_by_class_name('css-1vs4jn4')
        depart_time_elements = depart_time_box.find_elements(by=By.CSS_SELECTOR, value='*') 
        for time in depart_time_keys:
            for selector in depart_time_elements:
                if str(selector.get_attribute('innerHTML')).strip() == self.time_dict[time]:
                    selector.click()
        