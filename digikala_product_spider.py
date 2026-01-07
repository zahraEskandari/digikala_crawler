import os
import csv
import json
import time
import requests
from os.path import exists, join
from utility import delay
import re

class DigikalaProductSpider:

    CSV_DIR = "./csv/"
    OUT_DIR = "./product_jsonl/"

    BASE_URL = "https://api.digikala.com/v2/product/{}/"


    def __init__(self, start_page=None, end_page=None):
        self.start_page = start_page
        self.end_page = end_page
        self.is_range_base = start_page is not None and end_page is not None

        if not exists(self.OUT_DIR):
            os.mkdir(self.OUT_DIR)

        self.csv_files = sorted([
            f for f in os.listdir(self.CSV_DIR)
            if f.endswith(".csv")
        ])

    # -----------------------
    # helpers
    # -----------------------



    @staticmethod
    def extract_product_id(raw_value) -> int:
        """
        Accepts:
        - URL
        - dict-as-string
        - anything containing dkp-<digits>
        """
        # print('--------------------------------------------')
        # print(raw_value)
        raw_value = str(raw_value)   # ← VERY IMPORTANT
        match = re.search(r"dkp-(\d+)", raw_value)
        # print(match)
        # print('--------------------------------------------')
        if not match:
            raise ValueError(f"Cannot extract product id from: {raw_value}")
        return int(match.group(1))



    def fetch_product_detail(self, product_id: int):
        url = self.BASE_URL.format(product_id)
        print(url)
        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            },
            timeout=(5, 30)
        )
        r.raise_for_status()
        return r.json()["data"]["product"]

    # -----------------------
    # core
    # -----------------------

    def crawl(self):

        for i, csv_name in enumerate(self.csv_files):

            if self.is_range_base and not (self.start_page <= i < self.end_page):
                continue

            csv_path = join(self.CSV_DIR, csv_name)
            out_path = join(self.OUT_DIR, csv_name.replace(".csv", ".jsonl"))

            print(f"📦 Processing {csv_name}")

            # already done → skip
            if exists(out_path):
                print("   ⏭ exists, skipping")
                continue

            with open(csv_path, newline="", encoding="utf-8") as f_csv, \
                 open(out_path, "a", encoding="utf-8") as f_out:
                print(out_path)
                reader = csv.reader(f_csv)
                header = next(reader)  # skip header

                for row in reader:
                    try:
                        raw_uri = row[2]
                        product_id = self.extract_product_id(raw_uri)

                        product = self.fetch_product_detail(product_id)

                        f_out.write(
                            json.dumps(product, ensure_ascii=False) + "\n"
                        )

                        delay(1.8, 2.5)

                    except Exception as e:
                        print("❌ failed:", row[:3], e)


            print(f"✅ saved → {out_path}")
