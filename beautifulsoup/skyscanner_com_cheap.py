import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def fetch_skyscanner_content():
    url = "https://www.skyscanner.dk/transport/flights-from/cope/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=true&outboundaltsenabled=false&inboundaltsenabled=false&oym=1903&iym=1903&ref=home&fbclid=IwAR2mYnSGK7NZR0byLcHNMX9nwYmPVySvySr_LqyxmNiAJHo_fHuBw3kzYHc"
    temp_filename = "skyscanner_temp_file"
    # if os.path.isfile(temp_filename):
    #     return open(temp_filename, "r").read()

    webdriver_path = "chromedriver_win32/chromedriver_73.exe"
    browser = webdriver.Chrome(webdriver_path)

    # browser.set_window_size(800, 600)
    browser.get(url)
    element = WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "result-list"))
    )
    page_content = browser.page_source
    browser.close()

    skyscanner_dk_content = open(temp_filename, "w")
    skyscanner_dk_content.write(page_content)
    skyscanner_dk_content.close()
    return page_content


BLACK_LIST = ['Storbritannien', "Tyskland", "Irland"]
if __name__ == '__main__':
    flights = []

    page_content = fetch_skyscanner_content()
    product_page_soup = BeautifulSoup(page_content, 'html.parser')
    destination_elements = product_page_soup.find_all("div", class_="browse-data-route")
    for destination_element in destination_elements:
        name = destination_element.find("h3").get_text().strip()
        price_text = destination_element.find("p").get_text().strip()
        price = re.sub('[^0-9]', '', price_text)

        if name not in BLACK_LIST:
            if price and int(price) < 400:
                flights.append("{}: {}".format(name, price))

    subject = "FLIGHT_NOTIFICATION"
    message = "\n".join(flights)
    print(subject)
    print(message)
