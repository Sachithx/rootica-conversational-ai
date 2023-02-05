from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from search_engine.search_engine import SearchEngine
from api_endpoints.boto3_dynamodb import DynamoDBCRUD


def search(name):
    a = SearchEngine()
    tok_list, ids = a.preprocess()
    bm_25 = a.bm_25(tok_list)
    result = a.search(bm_25, name, ids)
    return result


class ActionAvailability(Action):

    def name(self) -> Text:
        return "action_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_product = tracker.get_slot("product")
        # current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x is not None:
            i = DynamoDBCRUD().get_product(x[0])
            if i.get('image') is not None:
                result = f"{i['product_name']} is Available. " \
                         f"{i['image']}" if i['available'] else f"Sorry! {i['product_name']} is Not Available."
            else:
                result = f"{i['product_name']} is Available. " \
                         f"No preview available!" if i['available'] else f"Sorry! {i['product_name']} is Not Available."
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
        # current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x is not None:
            i = DynamoDBCRUD().get_product(x[0])
            result = f"{i['product_name']} is good for {i['skin_type']}!" if i['skin_type'] is not None \
                else f"Sorry! {i['product_name']} skin type information is not available!"
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
        # current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x is not None:
            i = DynamoDBCRUD().get_product(x[0])
            result = f"{i['product_name']} is  Rs: {i['price']}!" if i['price'] is not None \
                else f"Sorry! {i['product_name']} Price is not available!"
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
        # current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x is not None:
            i = DynamoDBCRUD().get_product(x[0])
            result = "Ingredients of"+" " + i['product_name'] + "\n" + '\n'.join(i['ingredients']) \
                if i['ingredients'] is not None \
                else f"Sorry! {i['product_name']} Ingredients information is not available!"
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
        # current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x is not None:
            i = DynamoDBCRUD().get_product(x[0])
            result = f"Please click this link and purchase {i['product_name']} through our website:{i['checkout_url']}"\
                if i['checkout_url'] is not None else f"Sorry! {i['product_name']} purchase link is not available!"
        else:
            result = "Sorry! We cannot find the product. Please mention the Product you want and try again!"

        dispatcher.utter_message(text=result)

        return []


class ActionBenefits(Action):

    def name(self) -> Text:
        return "action_benefits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_product = tracker.get_slot("product")
        # current_product = next(tracker.get_latest_entity_values("product"), None)
        x = search(current_product)
        if x is not None:
            i = DynamoDBCRUD().get_product(x[0])
            result = f"{i['product_name']} Benefits: {i['benefits']}!" if i['benefits'] is not None \
                else f"Sorry! {i['product_name']} benefits information is not available!"
        else:
            result = "Sorry! We cannot find the product. Please mention the Product you want and try again!"

        dispatcher.utter_message(text=result)

        return []
