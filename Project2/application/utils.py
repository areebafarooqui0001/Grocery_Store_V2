from flask_restful import reqparse, fields

#----------Request parser for categories------------------------------------------------------
category_parser = reqparse.RequestParser()
category_parser.add_argument('name', type=str, help='Name should be a string', required=True)
category_parser.add_argument('description', type=str, help='Description should be a string', required=True)

#----------Request parser for products--------------------------------------------------------
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Product name')
parser.add_argument('description', type=str, help='Product description')
parser.add_argument('manufacture_date', type=str, help='Manufacture date')
parser.add_argument('expiry_date', type=str, help='Expiry date')
parser.add_argument('rate_per_unit', type=float, help='Rate per unit')
parser.add_argument('quantity', type=int, help='Quantity')

#----------Request parser for shopping cart items---------------------------------------------
shopping_cart_item_parser = reqparse.RequestParser()
shopping_cart_item_parser.add_argument('user_id', type=int, help='User ID')
shopping_cart_item_parser.add_argument('product_id', type=int, help='Product ID')
shopping_cart_item_parser.add_argument('quantity', type=int, help='Quantity')
shopping_cart_item_parser.add_argument('total', type=int, help='Total')

#------------------Raw Fields-----------------------------------------------------------------
class Creator(fields.Raw):
    def format(self, user):
        return user.email

class CategoryId(fields.Raw):
    def format(self, category):
        return category.name

class UserCart(fields.Raw):
    def format(self, user):
        return user.email

class ProductCart(fields.Raw):
    def format(self, product):
        return product.name


#----------marshal user data fields-----------------------------------------------------------
user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "active": fields.Boolean
}

#----------marshal category data fields-------------------------------------------------------
category_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'is_approved': fields.Boolean,
    'creator': Creator
}

#----------marshal category request data fields-----------------------------------------------
category_request_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'request': fields.String,
    'is_approved': fields.Boolean,
    'is_rejected': fields.Boolean,
    'creator_id': fields.Integer
}

#----------marshal product data fields--------------------------------------------------------
product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'manufacture_date': fields.DateTime,
    'expiry_date': fields.DateTime,
    'rate_per_unit': fields.Float,
    'quantity': fields.Integer,
    'category': fields.Nested(category_fields),
    'categoryid': CategoryId
}

#----------marshal cart item data fields------------------------------------------------------
shopping_cart_item_fields = {
    'id': fields.Integer,
    'user': UserCart,
    'product': ProductCart,
    'quantity': fields.Integer,
    'total': fields.Integer,
}

#----------marshal order data fields----------------------------------------------------------
order_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'total': fields.Float,
    'quantity': fields.Integer,
    'user_id': fields.Integer,
}