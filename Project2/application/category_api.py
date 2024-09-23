from flask_restful import Resource, marshal, abort
from flask import request
from .views import cache
from .models import Category, db, Product, StoreManagerRequest
from .auth import role_required, get_curr_user_id, get_curr_user_role
from .utils import category_fields, category_parser


class CategoryResource(Resource):
    @role_required(['admin', 'store_manager'])
    @cache.cached(timeout=30)
    def get(self):
        if 'id' in request.args:
            id = request.args.get('id')
            category = Category.query.filter_by(id=id).first()
            if category:
                return { 'name': category.name, 'description': category.description }, 200
            abort(404, message="Category not found")
        categories = Category.query.all()
        return {'categories': marshal(categories, category_fields)}

    @role_required(['admin', 'store_manager'])
    def post(self):
        token=request.headers.get('Authentication-Token')
        user_id = get_curr_user_id(token)
        user_role = get_curr_user_role(token)

        args = category_parser.parse_args()
        if user_role == "store_manager":
            manager_request = StoreManagerRequest(name=args.get("name", ""), 
                                            description=args.get("description", ""), 
                                            request="Create",
                                            creator_id=user_id)
            db.session.add(manager_request)
            db.session.commit()
            return {"message": "Category request submitted to admin"}, 200
        
        else: 
            category = Category(name=args.get("name", ""), 
                                description=args.get("description", ""), 
                                creator_id=user_id)
            db.session.add(category)
            db.session.commit()
            return {"message": "Category Created"}, 200

    @role_required(['admin', 'store_manager'])
    def put(self, category_id):
        user_id = get_curr_user_id(request.headers.get('Authentication-Token'))
        user_role = get_curr_user_role(request.headers.get('Authentication-Token'))

        category = Category.query.get(category_id)
        if not category:
            abort(404, message='Category not found')

        args = category_parser.parse_args()
        if user_role == "store_manager":
            args = category_parser.parse_args()
            manager_request = StoreManagerRequest(name=args.get("name", ""), 
                                            description=args.get("description", ""),
                                            category_id=category.id,
                                            request="Edit", 
                                            creator_id=user_id)
            db.session.add(manager_request)
            db.session.commit()
            return {"message": "Category request submitted to admin"}, 200
        else:
            category.name = args.get("name")
            category.description = args.get("description")
            for product in Product.query.filter_by(category_id=category_id).all():
                product.category_name = args.get("name")
                
            db.session.commit()
            return {"message": "Category updated"}, 200
            
    @role_required(['admin', 'store_manager'])
    def delete(self, category_id):
        user_id = get_curr_user_id(request.headers.get('Authentication-Token'))
        user_role = get_curr_user_role(request.headers.get('Authentication-Token'))

        category = Category.query.get(category_id)
        if not category:
            abort(404, message='Category not found')

        if user_role == "store_manager":
            manager_request = StoreManagerRequest(category_id=category.id,
                                                        name=category.name,
                                                        request="Delete", 
                                                        creator_id=user_id)
            db.session.add(manager_request)
            db.session.commit()
            return {"message": "Category request submitted to admin"}, 200
        else:
            db.session.delete(category)
            db.session.commit()
            return {"message": "Category deleted"}, 200
        
