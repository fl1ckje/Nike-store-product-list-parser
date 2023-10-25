from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions  import WebDriverException
import time

from data_manager import DataManager


SCROLL_PAUSE_TIME = 0.3
COOKIE_BTN_XPATH = '/html/body/div[3]/div/div[1]/div/div[2]/div/div[2]/div[2]/button'
PRODUCT_CARD_LINK_CSS = 'product-card__link-overlay'


class WebParser():
    def __init__(self, file_name: str, browser: str, home_url: str, url_load_timeout: int = 4):
        try:
            self.data_manager = DataManager()
            self.file_name = file_name
            if browser == 'chrome':
                options = webdriver.ChromeOptions()
                options.accept_insecure_certs = True
                driver = webdriver.Chrome(options)

            elif browser == 'chromium edge':
                driver = webdriver.ChromiumEdge()
            elif browser == 'edge':
                driver = webdriver.Edge()
            elif browser == 'firefox':
                driver = webdriver.Firefox()
            elif browser == 'ie':
                driver = webdriver.Ie()
            elif browser == 'safari':
                driver = webdriver.Safari()
            else:
                raise Exception('wrong web driver name')
            
            self.driver = driver
            self.driver.maximize_window()
            self.home_url = home_url

            if url_load_timeout >= 4:
                self.url_load_timeout = url_load_timeout
            else:
                self.url_load_timeout = 4

        except Exception as e:
            print(e)
            return


    def run(self):
        '''
        запуск парсера
        '''
        df = self.data_manager.read_data_from_xl(self.file_name)
        self.accept_cookies()

        for i in df.index:
            print(f"getting products links from [{i}]:\ncategory: {df['Категория'][i]}\nlink: {df['Ссылка'][i]}\n")
            products_links = self.get_category_products_links(df['Ссылка'][i])
            print(f"got {len(products_links)} links from category {df['Категория'][i]}")
            self.data_manager.write_data_to_xl(products_links, df['Категория'][i])
    

    def accept_cookies(self):
        '''
        принятие куки по домашней странице сайта
        '''
        print('accepting cookies...')
        try:
            self.driver.get(self.home_url)
            time.sleep(self.url_load_timeout)
            cookie_btn = self.driver.find_element(By.XPATH, COOKIE_BTN_XPATH)
            cookie_btn.click()
            print('cookie accept successful')

        except WebDriverException:
            print('cookie accept fail')
    

    def get_category_products_links(self, url: str):
        '''
        получение ссылок на все товары из категории по url
        '''
        print('loading category page...')
        self.driver.get(url)
        time.sleep(self.url_load_timeout)
        print('loaded category page. Scrolling...')

        new_scroll_height = 0
        prev_doc_scroll_height = 0
        current_doc_scroll_height = 0
        scroll_heights = []
        scroll_count = 0
        i = 0

        while True:
            new_scroll_height += 150
            self.driver.execute_script(f"window.scrollTo(0, {new_scroll_height});")
            current_doc_scroll_height = self.get_doc_scroll_height()
            scroll_heights.append(current_doc_scroll_height)
            scroll_count += 1

            if current_doc_scroll_height != prev_doc_scroll_height:
                print(f'did {scroll_count} scroll(s). Scrolled page to new height = {current_doc_scroll_height}...')
                prev_doc_scroll_height = current_doc_scroll_height
                scroll_count = 0
                scroll_heights.clear()

            if len(scroll_heights) > 50:
                if self.all_elements_equal(scroll_heights):
                    print("reached the end of page. Collecting products links...")
                    break
                else:
                    scroll_heights.clear()

            time.sleep(SCROLL_PAUSE_TIME)


        products_links = []
        i = 1

        for product_card in self.driver.find_elements(By.XPATH, f"//a[contains(@class, '{PRODUCT_CARD_LINK_CSS}')]"):
            link = product_card.get_attribute('href')
            products_links.append(link)
            i += 1

        return products_links
    

    def get_doc_scroll_height(self):
        return int(self.driver.execute_script("return document.documentElement.scrollHeight"))


    def all_elements_equal(self, list: list):
        return all(i == list[0] for i in list)
    

    def get_products_data_from_links(links, ):
        pass
