import glob
import os
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

ua = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'user-agent={ua.chrome}')
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    'download.default_directory': f'{os.getcwd()}/pdf_files',  # Change default directory for downloads
    'download.prompt_for_download': False,  # To auto download the file
    'download.directory_upgrade': True,
    'plugins.always_open_pdf_externally': True  # It will not show PDF directly in chrome
})
options.add_argument('start-maximized')
options.add_argument('--headless')


def search_data(
        product_title: str,
        url='https://inswiki.ru/index.php?id=15&search=%D1%81%D1%82%D0%B8%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D0%B0+atlant&searchbottom.x=0&searchbottom.y=0&searchbottom=submit',
        ):
    """
    ищет инструкцию по названию электроники и скачивает в пдф
    :param product_title: название электроники
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    move = ActionChains(driver)
    thumb = driver.find_element(By.XPATH, '//*[@id="js-rangeslider-js-0"]')
    move.click_and_hold(thumb).move_by_offset(200, 0).release().perform()
    input_ = driver.find_element(By.CLASS_NAME, 'search-input')
    driver.implicitly_wait(3)
    input_.send_keys(product_title)
    input_.send_keys(Keys.ENTER)
    element = driver.find_element(By.XPATH,
                                  '/html/body/div[1]/div[2]/div[2]/div[1]/h3/a')
    element.click()
    pdf = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[4]/span/a')
    pdf.click()
    time.sleep(10)

#
# file = glob.glob(f'{os.getcwd()}/pdf_files/*.pdf')
# os.remove(file[0])