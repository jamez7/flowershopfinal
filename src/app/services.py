from . import sql_db
from .models import CartItem, Product, Order

# Singleton zarządzający logiką koszyka zakupowego

class CartService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CartService, cls).__new__(cls)
        return cls._instance

    def add_item(self, session_id, product_id, quantity):
        product = Product.query.get(product_id)
        if not product:
            return None
        
        item = CartItem.query.filter_by(
            session_id=session_id, 
            product_id=product_id
        ).first()
        
        current_qty = item.quantity if item else 0
        new_total = current_qty + quantity
        
        if new_total > product.quantity:
            return 'insufficient_stock'
        
        if item:
            item.quantity = new_total
        else:
            item = CartItem(
                session_id=session_id,
                product_id=product_id,
                quantity=quantity
            )
            sql_db.session.add(item)
        
        sql_db.session.commit()
        return item

    def get_cart(self, session_id):
        return CartItem.query.filter_by(session_id=session_id).all()

    def remove_item(self, session_id, item_id):
        item = CartItem.query.filter_by(
            id=item_id, 
            session_id=session_id
        ).first()
        
        if item:
            sql_db.session.delete(item)
            sql_db.session.commit()
            return True
        return False

    def place_order(self, session_id):
        
        cart_items = self.get_cart(session_id)
        
        if not cart_items:
            return None
        
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if not product or product.quantity < item.quantity:
                return 'insufficient_stock'
        
        try:
            for item in cart_items:

                product = Product.query.get(item.product_id)
                product.quantity -= item.quantity
                
                order = Order(
                    session_id=session_id,
                    product_id=item.product_id,
                    quantity=item.quantity
                )
                sql_db.session.add(order)
            
            CartItem.query.filter_by(session_id=session_id).delete()
            
            sql_db.session.commit()
            return len(cart_items)
        
        except Exception as e:
            sql_db.session.rollback()
            return None