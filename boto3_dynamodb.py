import boto3
import json
from boto3.dynamodb.conditions import Attr
import os

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")
TABLE_NAME = "intern_challenge_sachith"
PRIMARY_COLUMN_NAME = "product_id"


class DynamoDBCRUD:
    def __init__(self) -> None:
        session = boto3.Session(
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_ACCESS_KEY,
            region_name='us-east-1'
            )

        client_dynamo = session.resource('dynamodb')
        self.table = client_dynamo.Table(TABLE_NAME)

    def json_to_dynamodb(self, path):
        """
        This function will send all the data in json file into DynamoDB Table.
        params:
          path: jason file path
        """
        # products = []
        with open(path, 'r') as f:
            products = json.load(f)
        f.close()

        for product in products:
            response = self.table.put_item(Item=product)
            print(response)
            print(f"Successfully added the data into DynamoDB Table: {TABLE_NAME}")

    def get_product(self, product_id):
        """
        This function will retrieve product information for a given product ID
        params:
          product_id: Product ID of required product
        returns:
          product information [dict]
        """
        try:
            response = self.table.get_item(
              Key={
                  PRIMARY_COLUMN_NAME: product_id
              }
                )
            product = response["Item"]
            return product

        except Exception as exception:
            return {'state': False, 'message': f'Cannot retrieve the Product.{exception}'}

    def create_product(self, product):
        """
        This function will create a new product in DynamoDB table for given information.
        params:
            {
                    product_id: int
                    product_name: Optional[str] = None
                    price: Optional[str] = None
                    benefits: Optional[str] = None
                    available: Optional[bool] = None
                    instructions: Optional[str] = None
                    skin_type: Optional[str] = None
                    ingredients: Optional[list] = None
                    image: Optional[str] = None
                    checkout_url: Optional[str] = None
            }
        returns:
            None
        """
        try:
            self.table.put_item(
                Item=product.dict(),
                ConditionExpression='attribute_not_exists(product_id)'
            )
            return {'state': True, 'message': "Created Successfully."}

        except Exception as e:
            return {'state': False, 'message': f"Couldn't create product. {e}"}

    def delete_product(self, product_id):
        """
        This function will delete the product for a given product ID.
        params:
          product_id: Product ID of required product to delete
        """
        try:
            self.table.delete_item(
                Key={
                    PRIMARY_COLUMN_NAME: product_id
                },
                ConditionExpression="attribute_exists(product_id)"
            )
            return {'state': True, 'message': "Successful"}
        except Exception as e:
            return {'state': False, 'message': f"Delete Unsuccessful. {e}"}

    def get_all(self):
        """
        This function will retrieve all the products with information in the table
        params:
          None
        returns:
          List of dictionaries of products
        """
        try:
            response = self.table.scan(
              FilterExpression=Attr('product_id').gte(0)
            )
            product_list = []
            for x in response["Items"]:
                product_list.append(x)
            product_dict = {}
            product_db = []
            for i in product_list:
                a = i.get('product_id')
                product_dict[a] = i
                product_db = product_dict
            return product_db
    
        except Exception as e:
            return {
                'state': False,
                'message': e
                }

    def update_product(self, product_id, product):
        """
        This function will update the information of an existing product
        in the DyanamoDB table.
        params:
            {
                    product_id: int
                    product_name: Optional[str] = None
                    price: Optional[str] = None
                    benefits: Optional[str] = None
                    available: Optional[bool] = None
                    instructions: Optional[str] = None
                    skin_type: Optional[str] = None
                    ingredients: Optional[list] = None
                    image: Optional[str] = None
                    checkout_url: Optional[str] = None
            }
        returns:
            None
        """
        try:
            self.table.update_item(
                Key={
                    PRIMARY_COLUMN_NAME: product_id
                },
                UpdateExpression="""SET 
                    product_name = :val1,
                    price = :val2,
                    benefits = :val3,
                    available = :val4,
                    instructions = :val5,
                    skin_type = :val6,
                    ingredients = :val7,
                    image = :val8,
                    checkout_url = :val9
                  """,
                ExpressionAttributeValues={
                    ":val1": product.get('product_name'),
                    ":val2": product.get('price'),
                    ":val3": product.get('benefits'),
                    ":val4": product.get('available'),
                    ":val5": product.get('instructions'),
                    ":val6": product.get('skin_type'),
                    ":val7": product.get('ingredients'),
                    ":val8": product.get('image'),
                    ":val9": product.get('checkout_url')
                  },
                ConditionExpression="attribute_exists(product_id)"
                    )
            return {'state': True, 'message': "Updated the product successfully."}

        except Exception as exception:
            return {'state': False, 'message': f"Couldn't update the Product. {exception}"}
