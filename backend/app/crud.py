"""
CRUD operations for database models
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from . import models, schemas


class OrderCRUD:
    """CRUD operations for Order model"""
    
    @staticmethod
    def get_all_orders(db: Session, skip: int = 0, limit: int = 100) -> List[models.Order]:
        """Get all orders with their products"""
        try:
            return db.query(models.Order)\
                .options(joinedload(models.Order.order_mappings).joinedload(models.OrderProductMap.product))\
                .offset(skip)\
                .limit(limit)\
                .all()
        except SQLAlchemyError as e:
            raise Exception(f"Database error while fetching orders: {str(e)}")
    
    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Optional[models.Order]:
        """Get order by ID with its products"""
        try:
            return db.query(models.Order)\
                .options(joinedload(models.Order.order_mappings).joinedload(models.OrderProductMap.product))\
                .filter(models.Order.id == order_id)\
                .first()
        except SQLAlchemyError as e:
            raise Exception(f"Database error while fetching order: {str(e)}")
    
    @staticmethod
    def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
        """Create a new order with products"""
        try:
            # Verify all products exist
            products = db.query(models.Product).filter(models.Product.id.in_(order.product_ids)).all()
            if len(products) != len(set(order.product_ids)):
                raise ValueError("One or more product IDs are invalid")

            # Create order
            db_order = models.Order(order_description=order.order_description)
            db.add(db_order)
            db.flush()  # Get the order ID

            # Create order-product mappings
            for product_id in order.product_ids:
                mapping = models.OrderProductMap(
                    order_id=db_order.id,
                    product_id=product_id,
                    quantity=1  # Default quantity is 1
                )
                db.add(mapping)

            db.commit()
            db.refresh(db_order)

            # Fetch with relationships
            order_id: int = db_order.id  # type: ignore
            return OrderCRUD.get_order_by_id(db, order_id)
        except ValueError as e:
            db.rollback()
            raise e
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Database error while creating order: {str(e)}")
    
    @staticmethod
    def update_order(db: Session, order_id: int, order_update: schemas.OrderUpdate) -> Optional[models.Order]:
        """Update an existing order"""
        try:
            db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
            if not db_order:
                return None

            # Update description if provided
            if order_update.order_description is not None:
                db_order.order_description = order_update.order_description  # type: ignore

            # Update products if provided
            if order_update.product_ids is not None:
                # Verify all products exist
                products = db.query(models.Product).filter(models.Product.id.in_(order_update.product_ids)).all()
                if len(products) != len(set(order_update.product_ids)):
                    raise ValueError("One or more product IDs are invalid")

                # Delete existing mappings
                db.query(models.OrderProductMap).filter(models.OrderProductMap.order_id == order_id).delete()

                # Create new mappings
                for product_id in order_update.product_ids:
                    mapping = models.OrderProductMap(
                        order_id=order_id,
                        product_id=product_id,
                        quantity=1  # Default quantity is 1
                    )
                    db.add(mapping)

            db.commit()

            # Fetch with relationships
            return OrderCRUD.get_order_by_id(db, order_id)
        except ValueError as e:
            db.rollback()
            raise e
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Database error while updating order: {str(e)}")
    
    @staticmethod
    def delete_order(db: Session, order_id: int) -> bool:
        """Delete an order"""
        try:
            db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
            if not db_order:
                return False
            
            db.delete(db_order)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Database error while deleting order: {str(e)}")


class ProductCRUD:
    """CRUD operations for Product model"""
    
    @staticmethod
    def get_all_products(db: Session) -> List[models.Product]:
        """Get all products"""
        try:
            return db.query(models.Product).all()
        except SQLAlchemyError as e:
            raise Exception(f"Database error while fetching products: {str(e)}")

