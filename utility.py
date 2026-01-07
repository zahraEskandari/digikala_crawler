import csv

import unicodedata
import re
import random
from time import sleep

def write_category_to_csv(file_dir, file_name, headers, rows):
    f = file_dir + f'{file_name}.csv'
    print(f'saving {f}' )
    with open(file_dir + f'{file_name}.csv', 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(rows)


# def delay(min_sec, max_sec=None):
#     if max_sec is None:
#         max_sec = min_sec
#     sleep(random.randint(min_sec, max_sec + 1))



def delay(min_sec=1.5, max_sec=2.0):
    sleep(random.uniform(min_sec, max_sec))
    
def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    value = re.sub(r'[-\s]+', '-', value).strip('-_')
    if len(value) > 50:
        value = value[0:50]
    return value
