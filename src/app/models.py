from . import sql_db

# Modele bazy danych - definicje tabel i relacji

# Product - katalog produktów (kwiaty) dostępnych w sklepie
# CartItem - tymczasowy koszyk zakupowy przypisany do sesji użytkownika
# Order - archiwum złożonych zamówień

class Product(sql_db.Model):

    id = sql_db.Column(sql_db.Integer, primary_key=True)
    name = sql_db.Column(sql_db.String(100), nullable=False)
    color = sql_db.Column(sql_db.String(50), nullable=False)
    description = sql_db.Column(sql_db.Text)
    image_path = sql_db.Column(sql_db.String(200))
    quantity = sql_db.Column(sql_db.Integer, default=0)

    def __repr__(self):
        return f'<Product {self.name}>'

class CartItem(sql_db.Model):

    id = sql_db.Column(sql_db.Integer, primary_key=True)
    session_id = sql_db.Column(sql_db.String(64), nullable=False, index=True)
    product_id = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('product.id'), nullable=False)
    quantity = sql_db.Column(sql_db.Integer, nullable=False, default=1)

    product = sql_db.relationship('Product')

    def __repr__(self):
        return f'<CartItem {self.quantity}x Product {self.product_id}>'

class Order(sql_db.Model):
    
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    session_id = sql_db.Column(sql_db.String(64), nullable=False, index=True)
    product_id = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('product.id'), nullable=False)
    quantity = sql_db.Column(sql_db.Integer, nullable=False)
    order_date = sql_db.Column(sql_db.DateTime, default=sql_db.func.now())
    
    product = sql_db.relationship('Product')
    
    def __repr__(self):
        return f'<Order {self.id}: {self.quantity}x Product {self.product_id}>'