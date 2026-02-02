from digikala_spider import DigikalaSpider
from multisprider import Multispider

if __name__ == "__main__":
    num_of_spiders = 15
   
    categories = DigikalaSpider.get_categories()
    total = len(categories)
    # divide work manually
    chunk = total // num_of_spiders
    spiders = []

    for i in range(num_of_spiders):
        start = i * chunk
        end = start + chunk
        spiders.append(DigikalaSpider(categories[start: end]))

    # last spider gets remainder
    spiders.append(DigikalaSpider(categories[end: total]))


    multispider = Multispider(spiders)
    multispider.multi_crawl()
