from typing import Optional
from fastapi import FastAPI
from models import Product
from function import CRUD
from boto3_dynamodb import DynamoDBCRUD

app = FastAPI()
boto3_dynamodb = DynamoDBCRUD()
#product_db = boto3_dynamodb.get_all()
crud = CRUD()

@app.get("/")
def get_product_query(limit: Optional[int] = None):
    """
    This function can retrieve all the products with details in the database.
    Optinally, we can set "limit" to number of products to show.
    """
    try:
        return crud.product_query()[:limit]
    except Exception as exeption:
        print(f"{exeption}")

@app.get("/products")
def get_product_path(product_id: int):
    """
    This function retrieves the product information for a given product ID.
    """
    try:
        if crud.product(product_id).get('state')==None:
            return crud.product(product_id)
        else:
            return {'state': False, 'message': "Getting product information is not successfull."}

    except Exception as exception:
        return {
            "state": False,
            "message": f"getting product information is not successfull. Error: {exception}"
            }

@app.post("/products")
def create_product(product: Product):
    """
    This can create new product for given product information, and save it in the database.
    """
    try:
        product_id = product.product_id
        if boto3_dynamodb.get_product(product_id).get('state')==False:
            if crud.create_product(product).get('state') == True:
                crud.create_product(product)
                return {'state':True,  'message': "Product cretated Successfully."}
            else:
                return {'state':False,  'message': "Couldn't create the product."}
        else:
            return {'state':False,  'message': "Couldn't create the product."}
    except Exception as exception:
        return {'state':False, 'message': f"Couldn't create the product. {exception}"}


@app.delete("/products")
def delete_product(product_id: int):
    """
    This can delete a product from the databse for a given product ID.
    """
    try:
        if crud.delete_product(product_id).get('state')==True:
            crud.delete_product(product_id)
            return {'state': True, 'message': f"Successfully deleted product: {product_id}"}
        else:
            return {'state': False, 'message': crud.delete_product(product_id).get('message')}
    except Exception as exception:
        return {'state': False, 'message': f"Couldn't deleted product: {product_id}: {exception}"}


@app.patch("/products")
def update_product_partial(product: Product):
    """
    This can edit or update an existing product for given information.
    """
    try:
        if crud.update_product(product).get('state')==True:
            crud.update_product(product)
            return {'state': True, 'message': f"Successfully updated the product"}
        else:
            return {'state': False, 'message':crud.update_product(product).get('message')}
    
    except:
        return {'state': False, 'message':f"Couldn't update the product."}
