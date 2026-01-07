import os
from lxml import html
from os.path import exists

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# from webdriver_manager.chrome import ChromeDriverManager

from category import Category
from utility import *


class DigikalaSpider:
    home_page_link = 'https://www.digikala.com/'

    product_info = ['نام', 'قیمت', 'وضعیت موجودی', 'امتیاز']
    max_page_num_per_category = 100

    home_page_delay = 5
    first_page_of_category_delay = 6
    min_page_delay = 2
    max_page_delay = 3
    try_page_delay = 1

    num_of_try_page_load = 4

    saved_file_dir = './csv/'

    xpaths = {
        'product_list':
            '//*[@id="base_layout_desktop_fixed_header"]/header/nav/div[1]/div[1]/div[1]/div/span',

        'category_form_1':
            '//*['
            '@class'
            '="BaseLayoutDesktopHeaderNavigationMainMegaMenu_BaseLayoutDesktopHeaderNavigationMainMegaMenu__item__DcC5_'
            ' BaseLayoutDesktopHeaderNavigationMainMegaMenu_BaseLayoutDesktopHeaderNavigationMainMegaMenu__item'
            '--main___jxDI d-flex text-body1-strong ai-center color-900 pos-relative mt-1"]',

        'category_form_2':
            '//*['
            '@class'
            '="BaseLayoutDesktopHeaderNavigationMainMegaMenu_BaseLayoutDesktopHeaderNavigationMainMegaMenu__item__DcC5_'
            ' text-body-2 color-500 mt-1"]',

        'product_block':
            '//*[@class="d-block pointer pos-relative bg-000 overflow-hidden grow-1 py-3 px-4 px-2-lg h-full-md '
            'styles_VerticalProductCard--hover__ud7aD"]',

        'product_name':
            '//*[@class="ellipsis-2 text-body2-strong color-700 '
            'styles_VerticalProductCard__productTitle__6zjjN"]/text()',

        'product_price':
            '//*[@class="d-flex ai-center jc-end gap-1 color-700 color-400 text-h5 grow-1"]/span/text()',

        'product_inventory':
            '//*[@class="d-flex ai-center jc-end gap-1 color-400 text-h5 grow-1"]/span/text()',

        'product_score':
            '//*[@class="text-body2-strong color-700"]/text()',

        'products_list_wrapper':
            '//*[@id="ProductListPagesWrapper"]/section[1]/div[1]/div/div/div',

        'pages_block':
            '//*[@class="font-body d-flex jc-center ai-center"]',

        'next_page_button':
            '//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[21]/div/div[3]',

        'category_name':
            'span/text()',

        'category_link':
            '@href'
    }

    def __init__(self, start_page=None, end_page=None) -> None:
        self.start_page = start_page
        self.end_page = end_page
        self.is_range_base = self.start_page is not None and self.end_page is not None

        options = self.get_browser_options()
        # self.browser = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        
        options = Options()

        # Tell Selenium to use Chromium (not Google Chrome)
        options.binary_location = "/usr/bin/chromium-browser"

        # Strongly recommended for crawlers
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = ChromeService("/usr/bin/chromedriver")

        self.browser = webdriver.Chrome(
            service=service,
            options=options
        )



    @staticmethod
    def get_browser_options():
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        return options

    def get_absolute_link(self, inner_link):
        return self.home_page_link + str(inner_link)

    def load_home_page(self):
        self.browser.get(self.home_page_link)
        delay(self.home_page_delay)

        product_list_elem = self.browser.find_element(By.XPATH, self.xpaths['product_list'])
        product_list_elem.click()
        delay(self.home_page_delay)

    

    def get_categories(self):
        from category import Category
        import requests

        url = "https://api.digikala.com/v1/search/"
        r = requests.get(
            url,
            params={"page": 1},
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
            },
            timeout=10,
        )

        payload = r.json()

        api_categories = (
            payload
            .get("data", {})
            .get("filters", {})        # ✅ correct key
            .get("categories", {})     # ✅ correct key
            .get("options", [])        # ✅ list of category dicts
        )

        categories = [
            Category(
                name=c.get("title_fa"),
                link=c.get("id")
            )
            for c in api_categories
            if c.get("title_fa") and c.get("code")
        ]

        return categories

        

    

    
    
    def get_category_products_data(self, category):
        print(category)
        import requests

        products_data = []
        self.max_page_num_per_category = 1
        for page in range(1, self.max_page_num_per_category + 1):
            r = requests.get(
                "https://api.digikala.com/v1/search/",
                params={
                    "categories[]": [category.link],
                    "page": page
                },
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                    "Accept": "application/json",
                },
                timeout=50
            )
                        

            data = r.json().get("data", {})

            products = data.get("products", [])
           
            if not products:
                break
            x = 0
            for p in products:
                print(x)
                x = x+1 
                products_data.append([
                    p.get("title_fa"),p.get("title_en"),p.get("url") , p.get('data_layer') , p.get('')
                    #p.get("price", {}).get("selling_price"), 
                    # "موجود" if p.get("status") == "marketable" else "ناموجود", 
                    #p.get("rating", {}).get("rate")
                ])
            print(products_data)
        return products_data



    def get_num_of_categories(self):        
        return len(self.get_categories())


    def crawl(self):

        # self.load_home_page()
        categories = self.get_categories()

        if not exists(self.saved_file_dir):
            os.mkdir(self.saved_file_dir)
            
        print(f'{self.saved_file_dir} Exists')

        for i, category in enumerate(categories):

            if self.is_range_base and not (self.start_page <= i < self.end_page):
                continue

            file_name = category.name + ' - ' + slugify(category.link, True).replace('search', '')
            # print(file_name)
            # print(category.link)
            print(self.saved_file_dir + file_name + '.csv')
            if not exists(self.saved_file_dir + file_name + '.csv'):
                products_data = self.get_category_products_data(category)
                print(products_data)
                if products_data:
                    write_category_to_csv(self.saved_file_dir, file_name,
                                          self.product_info, products_data)
        self.browser.close()
