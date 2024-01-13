from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

#! BASE MDDEL CLASS
class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str]=None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str]=None

# @app.get('/')
# def home():
#     return {"Data" : "Testing"}

# @app.get('/about')
# def about():
#     return {"Data" : "About"}


inventory = {}

#!GET METHODS
@app.get('/get-item/{item_id}/')
def get_item(item_id: int = Path( description="The id of the item you'd like to view", ge=1, lt=10)):
    return inventory[item_id]

# @app.get('/get-by-name/{item_id}')
# def get_item(*,item_id:int,name:str  , test = int):
#     for item_id in inventory:
#         if inventory[item_id].name == name:
#             return inventory[item_id]
#     raise HTTPException(status_code=404, detail="Item name not found")

@app.get('/get-by-name/')
def get_item(name: str = Query(None, title="Name", description="Name of the item.")):
    for item_id in inventory:
        if inventory[item_id].name ==  name:
            return inventory[item_id]
        raise HTTPException(status_code=404, detail="Item name not found")


#!POST METHOD API
@app.post('/create-item/{item_id}')
def create_item(item_id:int,item:Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item id already exists")
    
    inventory[item_id] = {"name" : item.name, "price" : item.price, "brand" : item.brand}
    return inventory[item_id]

#!PUT REQUEST API

@app.put('/update_item/{item_id}')
def update_item(item_id:int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item id does not exists")
    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]

@app.delete('/delete-item/')
def delete_item(item_id:int = Query(..., description="The ID of the item to delete", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item id does not exists")
    del inventory[item_id]
    return {"Success" : "Item deleted successfully"}