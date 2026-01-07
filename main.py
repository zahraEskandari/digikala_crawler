from digikala_spider import DigikalaSpider
from multisprider import Multispider

# if __name__ == '__main__':
#     num_of_spiders = 12
#     multispider = Multispider(num_of_spiders, DigikalaSpider().get_num_of_categories())
#     multispider.multi_crawl()


from digikala_spider import DigikalaSpider
from multisprider import Multispider

if __name__ == "__main__":
    num_of_spiders = 12
    total = DigikalaSpider().get_num_of_categories()

    # divide work manually
    chunk = total // num_of_spiders
    spiders = []

    for i in range(num_of_spiders):
        start = i * chunk
        end = start + chunk
        spiders.append(DigikalaSpider(start, end))

    # last spider gets remainder
    spiders[-1].end_page = total

    multispider = Multispider(spiders)
    multispider.multi_crawl()
