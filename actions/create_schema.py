import json
import html

class CreateSchema():
    def __init__(self, path):         
        # Opening JSON file
        f = open(path)
        # returns JSON object as a dictionary
        self.data = json.load(f)
        # Closing file
        f.close()

    def build(self):
        products_db = []
        for prod in self.data:
                dict = {
                        "product_id": None,
                        "product_name": None,
                        "price": None,
                        "benifits": None,
                        "available": None,
                        "instructions": None,
                        "skin_type": None,
                        "ingredients": None,
                        "image": None,
                        "checkout_url": None
                }

                ## Product ID
                dict["product_id"] = prod.get('id')      
                
                ## Product Name
                dict["product_name"] = html.unescape(prod.get('name'))           
                
                ## Price
                dict["price"] = prod.get('price') if len(prod.get('price'))!=0 else None

                ## Benifits
                for i in prod.get('meta_data'):
                    if i.get('key')=="product_components_0_details_0_description":
                        dict["benifits"] = i.get('value')
                        break

                ## Availability
                dict["available"] = True if prod.get('stock_status')=='instock' else False 

                ## Dosha Types
                for i in prod.get('attributes'):
                        if i.get('name')=="Dosha Types":
                                dict["skin_type"] = html.unescape(i.get('options')[0])

                ## Ingredients
                for i in prod.get('attributes'):
                        if i.get('name')=="Wonder Herbs":
                                dict["ingredients"] = i.get('options')  
                
                ## Images
                for i in prod.get('images'):
                        dict["image"] = prod.get('images')[0].get('src')

                ## Purchase Link
                dict["checkout_url"] = prod.get('permalink')

                products_db.append(dict)
        return products_db


