import requests
from getpass import getpass

def product_list():
    endpoint="http://localhost:8000/api/auth/"
    password=getpass()
    auth_response = requests.post(endpoint,json={"username":"admin","password":password})
    print(auth_response.text)

    if auth_response.status_code == 200:
        token = auth_response.json()["token"]
        headers={"Authorization":f"Bearer {token}"}
        endpoint = "http://localhost:8000/api/products/"
        get_response = requests.get(endpoint,headers=headers)
        print(get_response.text)

def product_item(pk=None):
    endpoint=f"http://localhost:8000/api/products/{pk}/"
    response = requests.get(endpoint)
    print(response.text)

def product_delete():
    product_id=input("enter product id")
    try:
        product_id=int(product_id)
    except:
        print(f'{product_id} is not a valid id')

    if product_id:
        endpoint=f"http://localhost:8000/api/products/{product_id}/delete/"
        response = requests.delete(endpoint)
        print(response.text)

def product_update(pk=None):
    endpoint=f"http://localhost:8000/api/products/{pk}/update/"
    data = {
        "title":"amazing product",
        'price':300}
    response = requests.put(endpoint, json=data)
    print(response.text)

def product_add():
    token= "09fe3b0a5298bc927c7050a351fef022b4f03f55"
    endpoint="http://localhost:8000/api/products/create/"
    headers = {"Authorization":f"Bearer {token}"}
    item={
        "title":"new product",
        "content":"this is fantastic product",
        "price":800,
        "sale_price":200,
        "my_discount":10.5}
    response = requests.post(endpoint,json=item,headers=headers)
    print(response.text)

product_add()
product_list()



