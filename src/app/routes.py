from flask import render_template, Blueprint, jsonify, url_for, request, session
from .models import Product
from . import sql_db
from .services import CartService

main_blueprint = Blueprint('main', __name__)

# Inicjalizacja serwisu koszyka (Singleton)

cart_service = CartService() 

# Identyfikator sesji użytkownika (do zarządzania koszykiem)

def get_session_id():
    sid = session.get('sid')
    if not sid:
        import uuid
        sid = uuid.uuid4().hex
        session['sid'] = sid
    return sid

# Strona główna wyświetlająca listę produktów

@main_blueprint.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Punkt końcowy API - pobieranie listy produktów

@main_blueprint.route('/api/products', methods=['GET'])
def api_get_products():
    products = Product.query.all()
    product_payload = []

    for product in products:
        product_payload.append({
            'id': product.id,
            'name': product.name,
            'color': product.color,
            'quantity': product.quantity,
            'description': product.description,
            'image_path': url_for('static', filename=product.image_path)
        })

    return jsonify(product_payload)

# Punkty końcowe API - pobieranie i modyfikacja zawartości koszyka

@main_blueprint.route('/api/cart', methods=['GET'])
def api_get_cart():
    session_id = get_session_id()
    items = cart_service.get_cart(session_id)

    payload = []
    for item in items:
        payload.append({
            'id': item.id,
            'product_id': item.product_id,
            'name': item.product.name,
            'quantity': item.quantity,
        })
    
    return jsonify(payload)


@main_blueprint.route('/api/cart', methods=['POST'])
def api_add_to_cart():
    data = request.get_json(force=True)
    product_id = data.get('product_id')
    qty = data.get('quantity', 1)
    
    if not product_id or qty <= 0:
        return jsonify({'error': 'Invalid product or quantity'}), 400
    
    session_id = get_session_id()
    result = cart_service.add_item(session_id, product_id, qty)
    
    if not result:
        return jsonify({'error': 'Product not found'}), 404
    
    if result == 'insufficient_stock':
        return jsonify({'error': 'Not enough stock'}), 400
    
    return jsonify({'message': 'Added to cart'}), 201


@main_blueprint.route('/api/cart/<int:item_id>', methods=['DELETE'])
def api_remove_from_cart(item_id):
    session_id = get_session_id()
    success = cart_service.remove_item(session_id, item_id)  # ← uses cart_service
    
    if not success:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify({'message': 'Removed from cart'}), 200


# Punkt końcowy API - składanie zamówienia

@main_blueprint.route('/api/orders', methods=['POST'])
def api_place_order():
    session_id = get_session_id()
    result = cart_service.place_order(session_id)
    
    if result is None:
        return jsonify({'error': 'Cart is empty or order failed'}), 400
    
    if result == 'insufficient_stock':
        return jsonify({'error': 'Not enough stock for some items'}), 400
    
    return jsonify({
        'message': 'Order placed successfully',
        'items': result
    }), 201