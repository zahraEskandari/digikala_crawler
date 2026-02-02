import json 
import io
import os
import pandas as pd
import traceback
id_list = []
title_fa_list = []
title_en_list = []
url_list = []
product_type_list = []

brand_id_list = []
brand_code_list = []
brand_title_fa_list = []
brand_title_en_list = []
brand_uri_list = []

category_id_list = []
category_code_list = []
category_title_fa_list = []
category_title_en_list = []

item_category2_list = []
item_category3_list = []
item_category4_list = []
item_category5_list = []


rating_rate_list = []
rating_count_list = []

colors_list = []

review_description_list = []
review_attributes_list = []

expert_reviews_description_list = []
expert_reviews_attributes_list = []

variants_list = []

main_image_urls_list = []
other_image_urls_list = []

product_list_dir = "./product_jsonl"
for i in os.scandir(product_list_dir):
    if i.is_file() : 
        print(f"Extracting product info from {i.path}")       
        cat_product_file = io.open(i.path)
        
        for line in cat_product_file.readlines():
            try:
                product_json_data = json.loads(line)
                id_list.append(product_json_data["id"])
                title_fa_list.append(product_json_data["title_fa"])
                title_en_list.append(product_json_data["title_en"])
                url_list.append(product_json_data["url"]["uri"])
                
                product_type_list.append(product_json_data["product_type"])
                
                brand_data = product_json_data.get("brand")

                if brand_data:
                    brand_id_list.append(brand_data["id"])
                else :
                    brand_id_list.append("")
                    
    
                if brand_data:
                    brand_code_list.append(brand_data["code"])
                else :
                    brand_code_list.append("")
                    
                if brand_data:
                    brand_title_fa_list.append(brand_data["title_fa"])
                else :
                    brand_title_fa_list.append("")
                    
                if brand_data:
                    brand_title_en_list.append(brand_data["title_en"])
                else :
                    brand_title_en_list.append("")
                    
                if brand_data:
                    brand_uri_list.append(brand_data["url"]["uri"])
                else :
                    brand_uri_list.append("")
                    
                
                
                category_id_list.append(product_json_data["category"]["id"])
                category_code_list.append(product_json_data["category"]["code"])
                category_title_fa_list.append(product_json_data["category"]["title_fa"])
                category_title_en_list.append(product_json_data["category"]["title_en"])
                
                item_category2_list.append(product_json_data["data_layer"]["item_category2"])
                item_category3_list.append(product_json_data["data_layer"]["item_category3"])
                item_category4_list.append(product_json_data["data_layer"]["item_category4"])
                item_category5_list.append(product_json_data["data_layer"]["item_category5"])
                
                rating_rate_list.append(product_json_data["rating"]["rate"])
                rating_count_list.append(product_json_data["rating"]["count"])
                
                colors_list.append(product_json_data["colors"])
                
                
                if isinstance((product_json_data["review"]) , {}.__class__ ) and product_json_data["review"].get("description"):
                    review_description_list.append(product_json_data["review"]["description"])
                else:
                    review_description_list.append("")
            
                if isinstance((product_json_data["review"]) , {}.__class__ ) and product_json_data["review"].get("attributes"):
                    review_attributes_list.append(product_json_data["review"]["attributes"])
                else:
                    review_attributes_list.append("")
                    
                    
                if isinstance((product_json_data["expert_reviews"]) , {}.__class__ ) and product_json_data["expert_reviews"].get("description"):
                    expert_reviews_description_list.append(product_json_data["expert_reviews"]["description"])
                else:
                    expert_reviews_description_list.append("")
            
                if isinstance((product_json_data["expert_reviews"]) , {}.__class__ ) and product_json_data["expert_reviews"].get("attributes"):
                    expert_reviews_attributes_list.append(product_json_data["expert_reviews"]["attributes"])
                else:
                    expert_reviews_attributes_list.append("")
                
                j = 0 
                variants = {}
                for variant in product_json_data["variants"] :
                    id = variant["id"]
                    color =  variant.get("color", "") 
                    seller_id = variant["seller"]["id"]
                    seller_code = variant["seller"]["code"]
                    price = variant["price"]["selling_price"]
                    variants[str(j)]=  {'id':id , 'color':color , 'seller_id':seller_id , 'seller_code' : seller_code , 'price': price}

                    j = j + 1
                variants_list.append(variants)  
                
             
                images_data = product_json_data.get("images", {})
                
                main_imgs_urls = []
                if isinstance(images_data, dict):
                    main_element = images_data.get("main", {})

                    raw_main_list = main_element.get("url", [])
                    
                    if isinstance(raw_main_list, list):
                        for img_item in raw_main_list:
                            if isinstance(img_item, str):
                                main_imgs_urls.append(img_item)

                
                            
                other_imgs_urls = []
                if isinstance(images_data, dict):
                    raw_list = images_data.get("list", [])
                    if isinstance(raw_list, list):
                        for img_item in raw_list:
                            if isinstance(img_item, dict):
                                # Again, 'url' is a list, so we take the first one
                                if isinstance(img_item.get("url"), list) and len(img_item["url"]) > 0:
                                    other_imgs_urls.append(img_item["url"][0])
                
            
                main_image_urls_list.append("||".join(main_imgs_urls)) 
                other_image_urls_list.append("||".join(other_imgs_urls)) 
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                print(line)


                        
            
        
df = pd.DataFrame({"id":id_list , "title_fa":title_fa_list , "title_en":title_en_list, 
                   "url":url_list ,"product_type":product_type_list, 
                   "brand_id": brand_id_list, "brand_code":brand_code_list,
                   "brand_title_fa":brand_title_fa_list , "brand_title_en":brand_title_en_list, "brand_uri":brand_uri_list,
                   "category_id":category_id_list , "category_code":category_code_list, 
                   "category_title_fa":category_title_fa_list, "category_title_en":category_title_en_list,
                   "item_category2":item_category2_list, "item_category3":item_category3_list, 
                   "item_category4":item_category4_list, "item_category5":item_category5_list,
                   "rating_rate" : rating_rate_list,
                   "rating_count" : rating_count_list,
                   "colors" : colors_list,
                   "review_description" :review_description_list,
                   "review_attributes":review_attributes_list,
                   "expert_reviews_description":expert_reviews_description_list,
                   "expert_reviews_attributes":expert_reviews_attributes_list,
                   "variants" : variants_list,
                   "main_image_urls": main_image_urls_list ,
                   "other_image_urls" : other_image_urls_list,
                
                   })

print(df.head())

df.to_csv("./products.csv" , sep='\t')     

