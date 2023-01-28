from boto3_dynamodb import DynamoDBCRUD
boto3_dynamodb = DynamoDBCRUD()
# database = boto3_dynamodb.get_all()

class CRUD():
    def __init__(self) -> None:
        """
        This is an initialisation of CRUD capablities.
        This gets an input of product databse.

        params:
        product_db : dictionary of all the products,
            key : Product ID
            value: Product Details as another dictionary.    
        """
        pass

    def product_query(self):
        """
        This outputs the set of all the products inside the databse.
        Also, it can get input of limit, which can limit number of products
        it should appear from the begining.
        params:
        product
        limit : integer
        """
        try:
            all_products = boto3_dynamodb.get_all()
            return list(all_products.values())
        
        except Exception as exception:
            return [
                {
                    'state': False,
                    'message': exception
                }
            ]
    
    def product(self, product_id):
        """
        This function retrieves the product information for a given product ID
        params:
            product_id: int
        returns:
            dictionary of all the information on the given product,
        """
        try:
            if boto3_dynamodb.get_product(product_id).get('state') == None:
                return boto3_dynamodb.get_product(product_id)
            else:
                return {'state': False, 'message': 'Cannot retrieve the Product.'}

        except Exception as exception:
            return {
                "state": False,
                "message": f"getting product information is not successfull. Error: {exception}"
                }

    def create_product(self, product):
        """
        This function can create a new product in the database on given product info.
        params:
            {
                    product_id: int
                    product_name: Optional[str] = None
                    price: Optional[str] = None
                    benifits: Optional[str] = None
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
            product_id = product.product_id
            if boto3_dynamodb.create_product(product).get('state')==True:
                boto3_dynamodb.create_product(product)
                return {'state': True, 'message': f"Successfully created product."}
            else:
                return {'state': False, 'message': f"Couldn't create the product."}

        except Exception as exception:
            return {'state': False, 'message': f"Couldn't create the product. {exception}"}

    def delete_product(self, product_id):
        """
        This function can delete a product for a given product ID
        params:
            product_id: int
        returns:
            None
        """
        try:
            if boto3_dynamodb.delete_product(product_id).get('state')==True:
                boto3_dynamodb.delete_product(product_id)
                return {'state': True, 'message': f"Successfully deleted product."}
            else:
                return {'state': False, 'message': boto3_dynamodb.delete_product(product_id).get('message')}

        except Exception as exception:
            return {'state': False, 'message': f"Couldn't deleted product: {product_id}: {exception}"}
    
    def update_product(self, product):
        """
        This function can edit product information inside each product.
        for given product.
        params:
            {
                    product_id: int
                    product_name: Optional[str] = None
                    price: Optional[str] = None
                    benifits: Optional[str] = None
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
            product_id = product.product_id
            print(product_id)
            old_product = boto3_dynamodb.get_product(product_id)
            old_product.update(product.dict(exclude_none=True))
            new_product = old_product
            if boto3_dynamodb.update_product(product_id, new_product).get('state')==True:
                boto3_dynamodb.update_product(product_id, new_product)
                return {'state': True, 'message': f"Successfully updated product"}
            else: return {'state': False, 'message': boto3_dynamodb.update_product(product_id, new_product).get('message')}
        
        except Exception as exception:
            print(exception)
            return {'state': False, 'message': f'Update unsuccessful. {exception}'}