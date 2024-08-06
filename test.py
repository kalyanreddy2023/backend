import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException

import pandas as pd
import logging 

url = 'https://admin.range-management.ingka.com/'


def login(wait):
    username = wait.until(EC.presence_of_element_located((By.ID, 'userNameInput')))
    username.send_keys(Keys.CONTROL + 'a')
    username.send_keys(Keys.CONTROL + 'x')
    username.send_keys('raram43' + '\n')

    password = wait.until(EC.presence_of_element_located((By.ID, 'passwordInput')))
    password.send_keys(Keys.CONTROL + 'a')
    password.send_keys(Keys.CONTROL + 'x')
    password.send_keys('Ram9914@' + '\n')


def get_data(item_code, country_codes):
    item_code = item_code.split(',')
    print(item_code)
    driver = None
    status_issue_list = []
    country_codes_list = []
    item_nos = []
    start_date_list = []
    end_date_list = []
    type_list = []
    global_start_date_list = []
    global_end_date_list = []
    image_src_list = []

    try:
        logging.info('webdriver0 exceuted')
        edge_options = Options()
       # edge_options.add_argument("--headless")
        print('code  debug49')
        driver = webdriver.Edge(options=edge_options)
        print('webdriver exceuted')

        # Open a webpage
        driver.get(url)
        print('webdriver2 exceuted')
        driver.maximize_window()
        print('webdriver3 exceuted')

        wait = WebDriverWait(driver, 15)

        try:
            # Inter Ikea button
            inter_ikea_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/section/div/div/div/div[3]/form[2]/button')))
            inter_ikea_button.click()
        except NoSuchElementException:
            print('Inter Ikea button not found')

        login(wait)
        # Privacy agreement button
        privacy_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[8]/div[3]/div/div[2]/div[2]/button/span')))
        privacy_button.click()

        country_code = 'GBL'
        for item in item_code:
            number = item
            country = country_codes
            # Select country button
            # print(f'Item No: {number}, country-code: {country}')
            if country_code != country:
                select_country_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f'/html/body/div/div[1]/div[1]/div/div[2]/button[2]')))
                select_country_button.click()
                # selector for Country
                country_button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'label[for="{country}"]')))
                country_button.click()
            country_code = country_codes

            # Input search and click
            find_search(driver, number)
            try:
                driver.implicitly_wait(3)
                checkbox = driver.find_element(By.ID, number)
                checkbox.click()
                # find_checkbox(driver, number)
            except Exception as e:
                print(e)
            try:
                status_issue = driver.find_element(By.XPATH,
                                                   '//*[@id="__next"]/div[2]/div[3]/div[2]/div[5]/div[2]/p').get_attribute(
                    'textContent')
            except NoSuchElementException:
                status_issue = 'NA'
            try:
                market_start_date = driver.find_element(By.XPATH,
                                                        '/html/body/div/div[2]/div[3]/div[2]/div[1]/div[3]/input').get_attribute(
                    "value")
            except NoSuchElementException:
                market_start_date = 'NA'
            try:
                market_end_date = driver.find_element(By.XPATH,
                                                      '/html/body/div/div[2]/div[3]/div[2]/div[2]/div[3]/input').get_attribute(
                    'value')
            except NoSuchElementException:
                market_end_date = 'NA'
            try:
                global_start_date = driver.find_element(By.XPATH,
                                                        '/html/body/div/div[2]/div[3]/div[2]/div[1]/div[1]/span[2]').get_attribute(
                    "textContent")
            except NoSuchElementException:
                global_start_date = 'NA'
            try:
                global_end_date = driver.find_element(By.XPATH,
                                                      '/html/body/div/div[2]/div[3]/div[2]/div[2]/div[1]/span[2]').get_attribute(
                    'textContent')
            except NoSuchElementException:
                global_end_date = 'NA'
            try:
                # driver.implicitly_wait(10)
                type_elements = driver.find_element(By.XPATH,
                                                    '/html/body/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[3]')
                type_value = type_elements.get_attribute('textContent')

                # type_value = ''
            except NoSuchElementException:
                type_value = 'NA'
            try:
                image = driver.find_element(By.CLASS_NAME, 'ImageWithStatus_itemImage___x2Kt')

                image_src = image.get_attribute('src')

            except NoSuchElementException:
                image_src = 'NA'

            # Print the data
            # print(f'Status (and issues): {status_issue}')
            # print('*' * 50)
            item_nos.append(number)
            type_list.append(type_value)
            country_codes_list.append(country_code)
            status_issue_list.append(status_issue)
            start_date_list.append(market_start_date)
            end_date_list.append(market_end_date)
            global_start_date_list.append(global_start_date)
            global_end_date_list.append(global_end_date)
            image_src_list.append(image_src)

        data = {
            'Item_no': item_nos,
            'Type': type_list,
            'Country_code': country_codes_list,
            'Status_code': status_issue_list,
            'Market_startdate': start_date_list,
            'Market_enddate': end_date_list,
            'Global_startdate': global_start_date_list,
            'Global_enddate': global_end_date_list,
            # 'Image_src': image_src_list
        }
        # df = pd.DataFrame(data=data)
        # print(df)
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def find_checkbox(driver, number):
    try:
        checkbox = driver.find_element(By.ID, number)
        checkbox.click()
    except Exception as e:
        find_checkbox(driver, number)

    finally:
        if driver is not None: 
            driver.quit()


def find_search(driver, number):
    try:
        search_input = driver.find_element(By.ID, 'id-input-search')
        # driver.execute_script("arguments[0].value = '';", search_input)
        search_input.send_keys(Keys.CONTROL + 'a')
        search_input.send_keys(Keys.CONTROL + 'x')
        search_input.send_keys(number + '\n')
    except Exception as e:
        find_search(driver, number)

# if __name__ == '__main__':
#     # numbers = ['90446563', '09291900', '99551093', '00017133']
#     # country = 'IE'
#     # input_df = pd.read_csv('input.csv', dtype={'Number': str})
#     # for row in input_df.index:
#     #     number = input_df['Number'][row]
#     #     country = input_df['Country Code'][row]
#     #     print(number, country)

#     # get_data_from_url(input_df)
#     numbers = '90446563'
#     country = 'IE'
#     df = get_data(numbers, country)
#     print(df)
