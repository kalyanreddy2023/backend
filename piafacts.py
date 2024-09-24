import time
import os

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.edge.options import Options
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

url = 'https://admin.range-management.ingka.com/'

def login_test(wait):
    username = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]')))
    username.send_keys(Keys.CONTROL + 'a')
    username.send_keys(Keys.CONTROL + 'x')
    username.send_keys('kalyan.paralapalli@ingka.com' + '\n')
    print('username entered')

    password = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input')))
    password.send_keys(Keys.CONTROL + 'a')
    password.send_keys(Keys.CONTROL + 'x')
    password.send_keys('KALamma@2024' + '\n')
    print('password entered')


def login(wait):
    username = wait.until(EC.presence_of_element_located((By.ID, 'userNameInput')))
    username.send_keys(Keys.CONTROL + 'a')
    username.send_keys(Keys.CONTROL + 'x')
    username.send_keys('kapar32')
    print('username enter')

    password = wait.until(EC.presence_of_element_located((By.ID, 'passwordInput')))
    password.send_keys(Keys.CONTROL + 'a')
    password.send_keys(Keys.CONTROL + 'x')
    password.send_keys('KALamma@2024' + '\n')
    print('password enter')


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
        edge_options = Options()
        edge_options.add_argument("--headless")
        # edge_options.add_argument("--disable-javascript")
        edge_options.add_argument('--disk-cache-dir=/path/to/cache')
        # Get the current working directory
        user_agent = "user-agent=[Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36]"
        edge_options.add_argument(user_agent)
         
        service = Service(EdgeChromiumDriverManager().install())
        browser = webdriver.Edge(service=service, options=edge_options)
        
        # Print the executable path of the Edge browserprint(service.path)  
        driver = webdriver.Edge(options=edge_options)
        browser.get('edge://version/')
        element = browser.find_element(By.ID, "profile_path")
        print('Print service path',service.path)
        print('pathelement',element.text)       
        # Open a webpage
        driver.get(url)
        driver.maximize_window()

        wait = WebDriverWait(driver, 15)
        #time.sleep(120)

        try:
            # Inter Ikea button
            inter_ikea_button = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/div/main/section/div/div/div/div[3]/form[1]/button')))
            inter_ikea_button.click()
        except NoSuchElementException:
            print('Inter Ikea button not found')

        # time.sleep(30)
        login_test(wait)
        # Privacy agreement button
        print('ikea button click')
        driver.implicitly_wait(5)
        html_content = driver.page_source
        print(html_content)
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
            status_issue = get_value(driver, 'By.XPATH',
                                     '/html/body/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div/div/div[3]/div[5]/span',
                                     'textContent')
            market_start_date = get_value(driver, 'By.XPATH',
                                          '/html/body/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div/div/div[3]/div[2]/span',
                                          'textContent')
            market_end_date = get_value(driver, 'By.XPATH',
                                        '/html/body/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div/div/div[3]/div[4]/span',
                                        'value')
            global_start_date = get_value(driver, 'By.XPATH',
                                          '/html/body/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div/div/div[3]/div[1]/span',
                                          'textContent')
            global_end_date = get_value(driver, 'By.XPATH',
                                        '/html/body/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div/div/div[3]/div[3]/span',
                                        'textContent')
            type_value = get_value(driver, 'By.XPATH',
                                   '/html/body/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[3]',
                                   'textContent')
            item_nos.append(number)
            type_list.append(type_value)
            country_codes_list.append(country_code)
            status_issue_list.append(status_issue)
            start_date_list.append(market_start_date)
            end_date_list.append(market_end_date)
            global_start_date_list.append(global_start_date)
            global_end_date_list.append(global_end_date)
            print(number, type_value, country_code, status_issue, market_start_date, market_end_date, global_start_date,
                  global_end_date)
            # image_src_list.append(image_src)

        data = {
            'Item_no': item_nos,
            'Type': type_list,
            'Country_code': country_codes_list,
            'Status_code': status_issue_list,
            'Market_startdate': start_date_list,
            'Market_enddate': end_date_list,
            'Global_startdate': global_start_date_list,
            'Global_enddate': global_end_date_list
            # 'Image_src': image_src_list
        }
        # df = pd.DataFrame(data=data)
        # print(df)
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()


def get_value(driver, by, path, attribute):
    for i in range(4):
        try:
            driver.implicitly_wait(1)
            # print(f'driver.find_element({by},{path}).get_attribute({attribute})')
            value = driver.find_element(By.XPATH, path).get_attribute(attribute)
            if value:
                return value
            else:
                return 'NA'
        except NoSuchElementException:
            # print("Could not find")
            time.sleep(1)
    return 'NA'


def find_checkbox(driver, number):
    try:
        checkbox = driver.find_element(By.ID, number)
        checkbox.click()
    except Exception as e:
        find_checkbox(driver, number)


def find_search(driver, number):
    try:
        search_input = driver.find_element(By.ID, 'id-input-search')
        # driver.execute_script("arguments[0].value = '';", search_input)
        search_input.send_keys(Keys.CONTROL + 'a')
        search_input.send_keys(Keys.CONTROL + 'x')
        search_input.send_keys(number + '\n')
    except Exception as e:
        find_search(driver, number)


if __name__ == '__main__':
    numbers = '20214571'
    country = 'CA'
    df = get_data(numbers, country)
    print('df',df)
(venv) kalyan_paralapalli@instance-20240823-095707:~/backend$ cat pia.py
cat: pia.py: No such file or directory
(venv) kalyan_paralapalli@instance-20240823-095707:~/backend$ ls -l
total 80
-rw-r--r-- 1 kalyan_paralapalli kalyan_paralapalli 8068 Sep  5 07:37 1
-rw-r--r-- 1 kalyan_paralapalli kalyan_paralapalli 1398 Sep  3 09:32 Dockerfile
-rw-r--r-- 1 kalyan_paralapalli kalyan_paralapalli   13 Sep  3 09:32 PAT.bat
drwxr-xr-x 2 kalyan_paralapalli kalyan_paralapalli 4096 Sep  5 08:02 __pycache__
-rw-r--r-- 1 kalyan_paralapalli kalyan_paralapalli 1535 Sep  3 09:32 app.py
-rw-r--r-- 1 kalyan_paralapalli kalyan_paralapalli  207 Sep  3 09:32 cloudbuild.yaml
drwxr-xr-x 3 kalyan_paralapalli kalyan_paralapalli 4096 Sep  3 09:32 edgedriver_win64
-rw-r--r-- 1 kalyan_paralapalli kalyan_paralapalli 8928 Sep  5 08:02 operara.py
drwxr-xr-x 4 kalyan_paralapalli kalyan_paralapalli 4096 Sep  3 09:32 pat_venv
drwxr-xr-x 3 kalyan_paralapalli kalyan_paralapalli 4096 Sep  5 06:37 path
-rw-r--r-- 1 kalyan_paralapalli kalyan_paralapalli 7007 Sep  3 09:32 piafacts.py
-rw-r--r-- 1 kalyan_paralapalli kalyan_paralapalli   30 Sep  3 09:32 requirement.bat
-rw-r--r-- 1 kalyan_paralapalli kalyan_paralapalli  725 Sep  3 09:32 requirement.txt
-rw-r--r-- 1 kalyan_paralapalli kalyan_paralapalli 8318 Sep  3 09:32 test.py
(venv) kalyan_paralapalli@instance-20240823-095707:~/backend$ cat piafacts.py
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
