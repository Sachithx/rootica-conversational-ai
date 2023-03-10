import json
import html


class CreateSchema:
    def __init__(self, path):         
        f = open(path)
        self.data = json.load(f)
        f.close()

    def build(self):
        products_db = []
        for prod in self.data:
            dic = {
                "product_id": prod.get('id'),
                "product_name": html.unescape(prod.get('name')),
                "price": prod.get('price') if len(prod.get('price')) != 0 else None,
                "benefits": None,
                "available": True if prod.get('stock_status') == 'instock' else False,
                "instructions": None,
                "skin_type": None,
                "ingredients": None,
                "image": prod.get('images')[0].get('src'),
                "checkout_url": prod.get('permalink')
                   }

            # Benefits
            for i in prod.get('meta_data'):
                if i.get('key') == "product_components_0_details_0_description":
                    dic["benefits"] = i.get('value')
                    break

            # Dosha Types
            for i in prod.get('attributes'):
                if i.get('name') == "Dosha Types":
                    dic["skin_type"] = html.unescape(i.get('options')[0])

            # Ingredients
            for i in prod.get('attributes'):
                if i.get('name') == "Wonder Herbs":
                    dic["ingredients"] = i.get('options')

            products_db.append(dic)
        return products_db
