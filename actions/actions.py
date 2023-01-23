import nltk.corpus.reader.wordnet as wn
from nltk.stem import WordNetLemmatizer
from rank_bm25 import BM25Okapi
import numpy as np
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from search_engine import SearchEngine
import json

def search(name):
    a = SearchEngine()
    tok_list, data = a.preprocess()
    bm_25 = a.bm_25(tok_list)
    result = a.search(bm_25, name, data)
    return result

### Custom actions ###
## Import the product database and do the transformations
f = open('products_db.json', 'r')
products_db = json.load(f)
f.close()

class ActionAvailability(Action):

    def name(self) -> Text:
        return "action_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_product = tracker.get_slot("product")
        #current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x != None:
            for i in products_db:
                if i['product_name']==x[0]:
                    if i.get('image')!=None:
                        result = f"{x[0]} is Available. {i['image']}" if i['available'] else f"Sorry! {x[0]} is Not Available."
                    else:
                        result = f"{x[0]} is Available. No preview available!" if i['available'] else f"Sorry! {x[0]} is Not Available."
        else:
            result = f"Sorry! We cannot find the product. Please mention the Product you want and try again!"

        dispatcher.utter_message(text=result)

        return []

class ActionSkinType(Action):

    def name(self) -> Text:
        return "action_skin_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_product = tracker.get_slot("product")
        #current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x != None:
            for i in products_db:
                if i['product_name']==x[0]:
                    result = f"{x[0]} is good for {i['skin_type']}!" if i['skin_type'] != None else f"Sorry! {x[0]} skin type information is not available!"
        else:
            result = "Sorry! We cannot find the product. Please mention the Product you want and try again!"

        dispatcher.utter_message(text=result)

        return []

class ActionPrice(Action):

    def name(self) -> Text:
        return "action_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_product = tracker.get_slot("product")
        #current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x != None:
            for i in products_db:
                if i['product_name']==x[0]:
                    result = f"{x[0]} is  Rs: {i['price']}!" if i['price'] != None else f"Sorry! {x[0]} Price is not available!"
        else:
            result = "Sorry! We cannot find the product. Please mention the Product you want and try again!"

        dispatcher.utter_message(text=result)

        return []

class ActionIngredients(Action):

    def name(self) -> Text:
        return "action_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_product = tracker.get_slot("product")
        #current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x != None:
            for i in products_db:
                if i['product_name']==x[0]:
                    result = "Ingredients of"+" "+ x[0]+"\n"+ '\n'.join(i['ingredients']) if i['ingredients']!= None else f"Sorry! {x[0]} Ingredients information is not available!"
        else:
            result = "Sorry! We cannot find the product. Please mention the Product you want and try again!"

        dispatcher.utter_message(text=result)

        return []

class ActionPurchase(Action):

    def name(self) -> Text:
        return "action_purchase"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_product = tracker.get_slot("product")
        #current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x != None:
            for i in products_db:
                if i['product_name']==x[0]:
                    result = f"Please click this link and purchase {x[0]} through our website: {i['checkout_url']}!" if i['checkout_url'] != None else f"Sorry! {x[0]} purchase link is not available!"
        else:
            result = "Sorry! We cannot find the product. Please mention the Product you want and try again!"

        dispatcher.utter_message(text=result)

        return []

class ActionBenifits(Action):

    def name(self) -> Text:
        return "action_benifits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_product = tracker.get_slot("product")
        #current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x != None:
            for i in products_db:
                if i['product_name']==x[0]:
                    result = f"{x[0]} Benifits: {i['benifits']}!" if i['benifits'] != None else f"Sorry! {x[0]} Benifits information is not available!"
        else:
            result = "Sorry! We cannot find the product. Please mention the Product you want and try again!"

        dispatcher.utter_message(text=result)

        return []