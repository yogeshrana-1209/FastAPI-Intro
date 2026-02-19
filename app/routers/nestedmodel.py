from typing import Tuple
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class supplier(BaseModel):
   supplierID:int
   supplierName:str

class product(BaseModel):
   productID:int
   prodname:str
   price:int
   supp:supplier

class customer(BaseModel):
   custID:int
   custname:str
   prod:Tuple[product]

# Return the Nested Model
@router.post('/invoice')
async def getInvoice(c1:customer):
   return c1