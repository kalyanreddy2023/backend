import time
import os

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select

import pandas as pd

url = 'https://piafacts.ikea.net/search'


def login(wait):
    username = wait.until(EC.presence_of_element_located((By.ID, 'userNameInput')))
    username.send_keys(Keys.CONTROL + 'a')
    username.send_keys(Keys.CONTROL + 'x')
    username.send_keys('user' + '\n')

    password = wait.until(EC.presence_of_element_located((By.ID, 'passwordInput')))
    password.send_keys(Keys.CONTROL + 'a')
    password.send_keys(Keys.CONTROL + 'x')
    password.send_keys('pwd' + '\n')


def get_data(item_code):
    item_code = item_code.split(',')
    print(item_code)
    driver = None
    item_code_list = []
    # sales_start_list = []
    # sales_end_list = []
    product_names = []
    ssd_eds_list = []
    image_list = []
    communicative_model_list = []
    try:
        # service = Service('chromedriver.exe')
        edge_options = Options()
        edge_options.add_argument("--headless")
        # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=edge_options)
        driver = webdriver.Edge(options=edge_options)
        current_path = os.getcwd()

        # Append the 'eddriver64' folder to the current path
        edgedriver_path = os.path.join(current_path, 'edgedriver_win64' ,'msedgedriver.exe')
        # Initialize the Edge WebDriver
        #driver = webdriver.Edge(executable_path=edge_driver_path)
        driver = webdriver.Edge(options=edge_options,executable_path=edgedriver_path)
        # driver = webdriver.Chrome(options=edge_options)
        driver.get(url)
        driver.maximize_window()

        wait = WebDriverWait(driver, 15)

        try:
            # Inter Ikea button
            inter_ikea_button = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/div/main/section/div/div/div/div[3]/form[1]/button')))
            inter_ikea_button.click()
        except NoSuchElementException:
            print('Inter Ikea button not found')
        # login(wait)
        try:
            select_element = wait.until(EC.presence_of_element_located((By.ID, 'unit-selector')))

            # Create a Select object for the <select> element
            select = Select(select_element)

            # Select the desired option by its label (visible text)
            option_label = "Official English"  # Replace with the label you want to select
            select.select_by_visible_text(option_label)
        except NoSuchElementException:
            print('select_language not found')
        for item in item_code:
            # print(item)
            find_search(driver, item)
            try:
                driver.implicitly_wait(2)
                span_product_name = driver.find_element(By.CSS_SELECTOR, '.facts__top-info h2')
                product_name_value = span_product_name.text
            except NoSuchElementException:
                product_name_value = 'NA'

            try:
                image = driver.find_element(By.CSS_SELECTOR,
                                            '.facts__image-gallery__main-picture .aspect-ratio-image__image')
                image_src = image.get_attribute('src')

            except NoSuchElementException:
                image_src = 'NA'

            try:
                # driver.implicitly_wait(2)
                span_sales_start = driver.find_element(By.XPATH,
                                                       f'//span[contains(text(), "Sales Start & Sales End")]/following-sibling::div/span')
                sales_start_value = span_sales_start.text
            except NoSuchElementException:
                sales_start_value = 'NA'
            try:
                span_sales_end = driver.find_element(By.XPATH,
                                                     f'//span[contains(text(), "Sales Start & Sales End")]/following-sibling::div/span[contains(@class, "text-")]')

                sales_end_value = span_sales_end.text

                # Remove the starting '-' character
                if sales_end_value.startswith('– '):
                    sales_end_value = sales_end_value[2:]
            except NoSuchElementException:
                sales_end_value = 'NA'

            try:
                div_element = driver.find_element(By.XPATH,
                                                  "//div[contains(@class, 'facts-documents__list-item') and .//span[contains(text(), 'Communicative 3DModel')]]")

                link_element = div_element.find_element(By.TAG_NAME, "a")
                communicative_link = link_element.get_attribute("href")

                # Print the href attribute
                print("Link:", communicative_link)
            except NoSuchElementException:
                communicative_link = 'NA'

            product_names.append(product_name_value)
            item_code_list.append(item)
            # sales_start_list.append(str(sales_start_value))
            # sales_end_list.append(str(sales_end_value).strip('-'))
            ssd_eds_list.append(f'{sales_start_value.strip()}-{sales_end_value.strip()}')
            image_list.append(image_src)
            communicative_model_list.append(communicative_link)
            # print('span_sales_start',sales_start_value)
        # time.sleep(10)
        data = {
            'item_code': item_code_list,
            'product_name': product_names,
            'ssd_eds': ssd_eds_list,
            'image_src': image_list,
            'communicative_link': communicative_model_list
        }
        # df = pd.DataFrame(data=data)
        # print(df)
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()


def find_search(driver, number):
    try:
        # search_input = driver.find_element(By.ID, 'item-search')
        search_input = driver.find_element(By.ID, 'search')
        # driver.execute_script("arguments[0].value = '';", search_input)
        search_input.send_keys(Keys.CONTROL + 'a')
        search_input.send_keys(Keys.CONTROL + 'x')
        search_input.send_keys(number + '\n')
    except Exception as e:
        find_search(driver, number)


if __name__ == '__main__':
    #     numbers = '12345,44881100,60510640,00542007,10542238,10531701,80507793'
    #     # country = 'IE'
    numbers = '20214571'
    df = get_data(numbers)
    print(df)
