import os
from os.path import exists


from category import Category
from utility import *


class DigikalaSpider:
    target_categories = []
    product_info = ['نام', 'قیمت', 'وضعیت موجودی', 'امتیاز']
    saved_file_dir = './csv/'


    def __init__(self, target_categories ) -> None:
        self.target_categories = target_categories

    @staticmethod
    def get_categories():
        from category import Category
        import requests

        url = "https://api.digikala.com/v1/search/?categories[]=1"
        r = requests.get(
            url,
            
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
            .get("filters", {})       
            .get("categories", {})     
            .get("options", [])        
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
        import requests

        products_data = []
        self.max_page_num_per_category = 5
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

                products_data.append([
                    p.get("title_fa"),p.get("title_en"), p.get("url") , p.get('data_layer') , p.get('')
                    
                ])
        return products_data

    def crawl(self):

        categories = self.target_categories

        if not exists(self.saved_file_dir):
            os.mkdir(self.saved_file_dir)
            
        print(f'{self.saved_file_dir} Exists')
        for i, category in enumerate(categories):
            file_name = category.name + ' - ' + slugify(category.link, True).replace('search', '')
            print(self.saved_file_dir + file_name + '.csv')
            if not exists(self.saved_file_dir + file_name + '.csv'):
                products_data = self.get_category_products_data(category)
                if products_data:
                    write_category_to_csv(self.saved_file_dir, file_name,
                                          self.product_info, products_data)


if __name__ =="__main__" : 
    print('Hi!')
    Categories = DigikalaSpider.get_categories()
    print(f'categories : ')
    print(len(Categories))
    print('Bye!')