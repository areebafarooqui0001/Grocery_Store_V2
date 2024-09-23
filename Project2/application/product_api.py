from flask_restful import Resource, marshal, abort
from flask import request, current_app as app
from .tasks import export_data
from .views import cache
from .models import Product, db, Category, User
from .auth import role_required, get_curr_user_id
from datetime import datetime
from .utils import product_fields, parser

class ProductResource(Resource):
    @role_required(['user', 'admin', 'store_manager'])
    @cache.cached(timeout=30)
    def get(self):
        if 'id' in request.args:
            id = request.args.get('id')
            product = Product.query.filter_by(id=id).first()
            if product:
                return {'product': marshal(product, product_fields) }, 200
            abort(404, message="Product not found")
        products = Product.query.all()
        return {'products': marshal(products, product_fields)}, 200 
    
    @role_required(['admin', 'store_manager'])
    def post(self):
        args = parser.parse_args()
        manufacture_date = datetime.strptime(args.get('manufacture_date'), '%Y-%m-%d')
        expiry_date = datetime.strptime(args.get('expiry_date'), '%Y-%m-%d') if args.get('expiry_date') else None
        category_id = request.json.get('category_id', None)
        if not category_id:
            abort(400, message="Category is required")

        category = Category.query.filter_by(id=category_id).first()
        if not category:
           abort(400, message="Category not found")

        product = Product(
            name=args.get('name'),
            description=args.get('description'),
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            rate_per_unit=args.get('rate_per_unit'),
            quantity=args.get('quantity'),
            category_name=category.name,
            category_id=category_id
        )
        db.session.add(product)
        db.session.commit()
        return {"message": "Product Created"}, 200

    @role_required(['admin', 'store_manager'])
    def put(self, product_id):
        args = parser.parse_args()
        
        product = Product.query.get(product_id)
        if product:
            product.name = args.get('name')
            product.description = args.get('description')
            # product.manufacture_date = args.get('manufacture_date')
            # product.expiry_date = args.get('expiry_date')
            product.rate_per_unit = args.get('rate_per_unit')
            product.quantity = args.get('quantity')
            db.session.commit()
            return {"message": "Product updated"}, 200
        abort(404, message='Product not found')
    
    @role_required(['admin', 'store_manager'])
    def delete(self, product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return {'message': 'Product deleted successfully'}, 200
        abort(404, message='Product not found')
        
class StoreManagerDataResource(Resource):
    @role_required(['store_manager'])  
    @cache.cached(timeout=30)
    def get(self):
        user_id = get_curr_user_id(request.headers.get('Authentication-Token'))
        user = User.query.get(user_id)

        fetched_categories = Category.query.filter_by(creator_id=user_id).all()
        categories = []
        for category in fetched_categories:
            categories.append([category.name, category.description])
        export_data(categories, user.email, user.username.split()[0])

        return {'message': 'Details sent to your mail.'}, 200


@app.before_request
def clear_cache_for_non_get():
    if request.method != 'GET':
      cache.clear()
      pass