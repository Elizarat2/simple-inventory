from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Item

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/')
def index():
    return render_template('index.html')


@inventory_bp.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200


@inventory_bp.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({"error": "El campo 'name' es obligatorio"}), 400

    item = Item(
        name=name,
        quantity=data.get('quantity', 0),
        price=data.get('price', 0.0),
        category=data.get('category'),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@inventory_bp.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json() or {}
    item.name = data.get('name', item.name)
    item.quantity = data.get('quantity', item.quantity)
    item.price = data.get('price', item.price)
    item.category = data.get('category', item.category)
    db.session.commit()
    return jsonify(item.to_dict()), 200


@inventory_bp.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item eliminado"}), 200