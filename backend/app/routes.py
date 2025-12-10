"""
API routes for the e-commerce application
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import schemas, crud
from .database import get_db

router = APIRouter()


@router.get("/orders", response_model=List[schemas.OrderResponse], tags=["Orders"])
async def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all orders with their associated products

    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        orders = crud.OrderCRUD.get_all_orders(db, skip=skip, limit=limit)

        # Transform to response format
        response = []
        for order in orders:
            products = [mapping.product for mapping in order.order_mappings]

            response.append(schemas.OrderResponse(
                id=order.id,  # type: ignore
                order_description=order.order_description,  # type: ignore
                created_at=order.created_at,  # type: ignore
                products=products  # type: ignore
            ))

        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch orders: {str(e)}"
        )


@router.get("/orders/{order_id}", response_model=schemas.OrderResponse, tags=["Orders"])
async def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific order by ID with its associated products

    - **order_id**: The ID of the order to retrieve
    """
    try:
        order = crud.OrderCRUD.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found"
            )

        # Transform to response format
        products = [mapping.product for mapping in order.order_mappings]

        return schemas.OrderResponse(
            id=order.id,  # type: ignore
            order_description=order.order_description,  # type: ignore
            created_at=order.created_at,  # type: ignore
            products=products  # type: ignore
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch order: {str(e)}"
        )


@router.post("/orders", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED, tags=["Orders"])
async def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new order with associated products
    
    - **order_description**: Description of the order
    - **product_ids**: List of product IDs to associate with the order
    """
    try:
        db_order = crud.OrderCRUD.create_order(db, order)
        
        # Transform to response format
        products = [mapping.product for mapping in db_order.order_mappings]
        return schemas.OrderResponse(
            id=db_order.id,  # type: ignore
            order_description=db_order.order_description,  # type: ignore
            created_at=db_order.created_at,  # type: ignore
            products=products  # type: ignore
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create order: {str(e)}"
        )


@router.put("/orders/{order_id}", response_model=schemas.OrderResponse, tags=["Orders"])
async def update_order(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing order

    - **order_id**: The ID of the order to update
    - **order_description**: New description (optional)
    - **product_ids**: New list of product IDs (optional)
    """
    try:
        db_order = crud.OrderCRUD.update_order(db, order_id, order_update)
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found"
            )

        # Transform to response format
        products = [mapping.product for mapping in db_order.order_mappings]
        return schemas.OrderResponse(
            id=db_order.id,  # type: ignore
            order_description=db_order.order_description,  # type: ignore
            created_at=db_order.created_at,  # type: ignore
            products=products  # type: ignore
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update order: {str(e)}"
        )


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Orders"])
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an order by ID

    - **order_id**: The ID of the order to delete
    """
    try:
        success = crud.OrderCRUD.delete_order(db, order_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete order: {str(e)}"
        )


@router.get("/products", response_model=List[schemas.ProductResponse], tags=["Products"])
async def get_all_products(db: Session = Depends(get_db)):
    """
    Get all available products
    """
    try:
        products = crud.ProductCRUD.get_all_products(db)
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch products: {str(e)}"
        )

