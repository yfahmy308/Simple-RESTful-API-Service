from flask import Blueprint, request, jsonify
from .models import Product, db

bp = Blueprint('routes', __name__)

@bp.route('/resource', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('description'):
        return jsonify({"error": "Missing name or description"}), 400
    
    # Check for duplicate product name
    if Product.query.filter_by(name=data['name']).first():
        return jsonify({"error": "Product with this name already exists"}), 400

    new_product = Product(name=data['name'], description=data['description'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify(new_product.to_dict()), 201

@bp.route('/resource', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

@bp.route('/resource/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)  # Updated for SQLAlchemy 2.0
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict()), 200

@bp.route('/resource/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = db.session.get(Product, id)  # Updated for SQLAlchemy 2.0
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify(product.to_dict()), 200

@bp.route('/resource/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)  # Updated for SQLAlchemy 2.0
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200
