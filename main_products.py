from digikala_product_spider import DigikalaProductSpider
from multisprider import Multispider

if __name__ == "__main__":
    num_spiders = 2

    base = DigikalaProductSpider()
    ranges = []

    total = len(base.csv_files)
    step = total // num_spiders

    for i in range(num_spiders):
        start = i * step
        end = total if i == num_spiders - 1 else (i + 1) * step
        ranges.append((start, end))

    spiders = [
        DigikalaProductSpider(start, end)
        for start, end in ranges
    ]

    Multispider(spiders).multi_crawl()
