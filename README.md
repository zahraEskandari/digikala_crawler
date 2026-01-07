# Digikala Crawler

This project is a Python-based crawler for extracting category data, product lists, and full product details from Digikala using official Digikala APIs.

The crawler is designed to:
- Fetch product categories
- Fetch products within each category
- Fetch full product details
- Store data locally for further analysis or downstream processing

---

## APIs Used

This project uses the following Digikala APIs:

### 1. Get categories
https://api.digikala.com/v1/search/

Used to retrieve available product categories via filters.

---

### 2. Get products within a category
https://api.digikala.com/v1/search/?categories[]=77&page=1

Parameters:
- categories[] → category ID
- page → pagination index

Used to retrieve product lists for each category.

---

### 3. Get product details
https://api.digikala.com/v2/product/19500751/

Used to retrieve full product details including specifications, attributes, descriptions, pricing, and metadata.

⚠️ Important: The trailing / at the end of the URL is required.

---

## Project Structure

- digikala_spider.py  
  Crawls categories and product lists per category.

- digikala_product_spider.py  
  Reads category CSV files and fetches full product details.

- multispider.py  
  Handles multithreaded execution of spiders.

- utility.py  
  Shared helper functions (delays, CSV writing, etc.).

- csv/  
  Generated CSV files containing category product lists (ignored by git).

- product_jsonl/  
  Generated JSONL files containing product details (ignored by git).

---



## Credits

This project heavily uses and is inspired by the following repository:

https://github.com/HB-2000/digikala_crawler/

The structure and crawling logic have been adapted and extended to support:
- API-first crawling
- Product detail extraction
- Multithreaded execution

---

## Notes

- This project is intended for educational and research purposes.
- Be mindful of Digikala request limits.
- Use delays and multithreading responsibly.





## How to Run

### 1. Crawl categories & product lists
This step saves **~20 products per category** into CSV files.

```bash
python main.py
```

Output:
```
./csv/<category_name>-<category_id>.csv
```

---

### 2. Crawl product details
This step reads CSV files and fetches **full product details**.
Each product is saved as **one JSON per line**.

```bash
python main_products.py
```

Output:
```
./product_jsonl/<category_name>-<category_id>.jsonl
```

---

## Notes
- Product detail API **requires trailing slash**:
  ```
  https://api.digikala.com/v2/product/<id>/
  ```
- Crawling is multi-threaded using `Multispider`
- Delays are intentionally added to reduce API pressure