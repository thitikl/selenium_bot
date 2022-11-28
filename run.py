from booking.booking import Booking
import time
from selenium.common.exceptions import StaleElementReferenceException

try:
    with Booking(quit_browser=False) as bot:
        bot.land_first_page()
        # bot.change_currency(currency='USD')
        bot.search_airport(
            flight_origin='bangkok',
            flight_destination='tokyo'
        )
        bot.search_date('2022-12-15')
        time.sleep(0.5)
        bot.click_search()
        # # bot.filter()
        # time.sleep(2)
        # bot.report_result()

except Exception as e:
    if 'PATH' in str(e):
        print('There is an error in PATH of driver')
    else:
        raise
