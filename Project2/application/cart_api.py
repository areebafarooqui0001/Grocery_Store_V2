from flask_restful import Resource, marshal
from flask import request
from .views import cache
from .models import Product, db, ShoppingCartItem, Order
from .auth import role_required, get_curr_user_id
from .utils import shopping_cart_item_fields, shopping_cart_item_parser, order_fields

class ShoppingCartItemResource(Resource):
    @role_required(['user'])
    @cache.cached(timeout=180)
    def get(self):
        user_id = get_curr_user_id(request.headers.get('Authentication-Token'))
        cart_items = ShoppingCartItem.query.filter_by(user_id=user_id).all()
        cart_total = 0
        for cart_product in cart_items:
            cart_total += cart_product.total
        return { 'cart_products': marshal(cart_items, shopping_cart_item_fields),
                'cart_total': cart_total}, 200

    @role_required(['user'])
    def post(self):
        user_id = get_curr_user_id(request.headers.get('Authentication-Token'))
        args = shopping_cart_item_parser.parse_args()
        product_id = args.get("product_id")
        quantity = args.get("quantity")
        total = args.get("total")

        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found"}, 404

        existing_item = ShoppingCartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.total += total
        else:
            new_item = ShoppingCartItem(user_id=user_id, product_id=product_id, quantity=quantity,total=total)
            db.session.add(new_item)

        db.session.commit()
        return {"message": "Item added to your cart"}

    @role_required(['user'])
    def put(self, item_id):
        args = shopping_cart_item_parser.parse_args()
        quantity = args.get("quantity")

        cart_item = ShoppingCartItem.query.get(item_id)
        if cart_item:
            cart_item.quantity = quantity
            db.session.commit()
            return {"message": "Item updated on cart"}, 200
        else:
            return {"message": "Cart item not found"}, 404

    @role_required(['user'])
    def delete(self, item_id):
        cart_item = ShoppingCartItem.query.get(item_id)
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return {"message": "Item deleted from cart"}, 200
        else:
            return {"message": "Cart item not found"}, 404
     

class PurchaseCartResource(Resource):
    @role_required(['user'])
    def get(self):
        user_id = get_curr_user_id(request.headers.get('Authentication-Token'))
        orders = Order.query.filter_by(user_id=user_id).all()
        return marshal(orders, order_fields), 200
    
    @role_required(['user'])
    def post(self):
        user_id = get_curr_user_id(request.headers.get('Authentication-Token'))
        cart_items = ShoppingCartItem.query.filter_by(user_id=user_id).all()

        for cart_product in cart_items:
            product = Product.query.get(cart_product.product_id)
            if product and product.quantity >= cart_product.quantity:
                new_order = Order(name=product.name, 
                                  quantity=cart_product.quantity,
                                  total=cart_product.total,
                                  user_id=user_id)
                db.session.add(new_order)
                product.quantity = product.quantity - cart_product.quantity
            db.session.delete(cart_product)
        db.session.commit()
        return {"message": "Products purchased successfully"}, 200