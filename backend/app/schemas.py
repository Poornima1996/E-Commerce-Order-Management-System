"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


# Product Schemas
class ProductBase(BaseModel):
    """Base product schema"""
    product_name: str = Field(..., max_length=100, description="Product name")
    product_description: Optional[str] = Field(None, description="Product description")


class ProductResponse(ProductBase):
    """Product response schema"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# Order Schemas
class OrderCreate(BaseModel):
    """Schema for creating an order"""
    order_description: str = Field(..., max_length=100, min_length=1, description="Order description")
    product_ids: List[int] = Field(..., min_length=1, description="List of product IDs")


class OrderUpdate(BaseModel):
    """Schema for updating an order"""
    order_description: Optional[str] = Field(None, max_length=100, min_length=1, description="Order description")
    product_ids: Optional[List[int]] = Field(None, min_length=1, description="List of product IDs")


class OrderResponse(BaseModel):
    """Order response schema"""
    id: int
    order_description: str
    created_at: datetime
    products: List[ProductResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Error Response Schema
class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str = Field(..., description="Error message")


# Success Response Schema
class SuccessResponse(BaseModel):
    """Success response schema"""
    message: str = Field(..., description="Success message")

