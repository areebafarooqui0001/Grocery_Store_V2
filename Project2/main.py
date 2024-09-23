from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS
from application.worker import celery_app
from application.models import db, Role, User
from werkzeug.security import generate_password_hash
from config import DevelopmentConfig
import uuid


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(DevelopmentConfig)

    api = Api(app)
    db.init_app(app)
    app.app_context().push()
    return app, api

app, api = create_app()
app.app_context().push()

from application.views import *



from application.cart_api import ShoppingCartItemResource, PurchaseCartResource
api.add_resource(ShoppingCartItemResource, '/api/shopping_cart_items', '/api/shopping_cart_items/<int:item_id>')
api.add_resource(PurchaseCartResource, '/api/order_history', '/api/cart_purchase')

from application.category_api import CategoryResource
api.add_resource(CategoryResource, '/api/categories', '/api/categories/<int:category_id>')

from application.product_api import ProductResource, StoreManagerDataResource
api.add_resource(ProductResource, '/api/products', '/api/products/<int:product_id>')
api.add_resource(StoreManagerDataResource, '/api/store_manager_export')


def create_initial_roles_and_admin():
    if len(Role.query.all()) < 3:
      role1 = Role(name='user', description='This is a customer')
      role2 = Role(name='admin', description='This is admin')
      role3 = Role(name='store_manager', description='This is store_manager')

      db.session.add_all([role1, role2, role3])
      db.session.commit()

    admin_role = Role.query.filter_by(name='admin').first()
    admin_user = User.query.filter_by(email='admin@email.com').first()

    if admin_role and not admin_user:
        hashed_password = generate_password_hash('admin')
        admin = User(username='Admin', email='admin@email.com', 
                     password=hashed_password, 
                     active=True,
                     fs_uniquifier=str(uuid.uuid4()))
        admin.roles.append(admin_role)
        db.session.add(admin)
        db.session.commit()
    print('DB is okay.')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_initial_roles_and_admin()
    app.run(debug=True, port=8080)
