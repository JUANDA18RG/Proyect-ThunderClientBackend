from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from db import product_collection, product_helper
from models import Product
from typing import List

router = APIRouter()


@router.get("/products", response_model=List[Product])
async def get_products():
    products = []
    async for product in product_collection.find():
        products.append(product_helper(product))
    return products


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await product_collection.find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_helper(product)


@router.post("/products", response_model=Product)
async def create_product(product: Product = Body(...)):
    product = jsonable_encoder(product)
    new_product = await product_collection.insert_one(product)
    created_product = await product_collection.find_one({"_id": new_product.inserted_id})
    return product_helper(created_product)


@router.put("/products/{code}", response_model=Product)
async def update_product(code: str, product: Product = Body(...)):
    product_data = {k: v for k, v in product.dict().items() if v is not None}
    updated_product = await product_collection.update_one({"code": code}, {"$set": product_data})
    if updated_product.modified_count == 1:
        updated_product = await product_collection.find_one({"code": code})
        return product_helper(updated_product)
    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/products/{code}", response_model=Product)
async def delete_product(code: str):
    product = await product_collection.find_one({"code": code})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await product_collection.delete_one({"code": code})
    return product_helper(product)
