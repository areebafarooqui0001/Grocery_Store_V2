from flask import current_app as app, jsonify, request
from flask_restful import marshal
from flask_caching import Cache
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Role, Category, StoreManagerRequest, Product
from .auth import get_token, role_required
from .utils import user_fields, category_request_fields
import uuid

cache = Cache(app)

@app.post('/user-register')
def user_register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role', 'user')  # Default role=='user' if not provided any

    if not email or not password or not name:
        return jsonify({"message": "Incomplete registration data"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User with this email already exists"}), 409

    # --------------to check if the provided role is valid in your system--------------------
    valid_roles = ['user', 'admin', 'store_manager']
    if role not in valid_roles:
        return jsonify({"message": "Invalid role for user"}), 400

    if role == 'user':
        user = User(email=email, password=generate_password_hash(password), 
                    username=name, fs_uniquifier=str(uuid.uuid4()), active=True)
    else:
        user = User(email=email, password=generate_password_hash(password), 
                    username=name, fs_uniquifier=str(uuid.uuid4()))

    user.roles.append(Role.query.filter_by(name=role).first())  # Assign the selected role
    db.session.add(user)

    try:
        db.session.commit()
        if role == 'store_manager':
            return jsonify({"message": "Registration successful. Waiting for admin approval."}), 200
        else:
            return jsonify({"message": "Registration successful"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error while registration: {str(e)}"}), 500

 
@app.route('/user-login', methods=['POST'])
def user_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email/Password not provided"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User Not Found"}), 404

    if check_password_hash(user.password, password):
        if user.roles[0].name == "store_manager" and not user.active:
            if user.is_rejected:
                return jsonify({"message": "Your request is rejected"}), 400
            return jsonify({"message": "Your approval is pending"}), 400

        roles = [role.name for role in user.roles]
        token = get_token(user.id, roles)
        return jsonify({"token": token, "email": user.email, "role": user.roles[0].name}), 200
    else:
        return jsonify({"message": "Incorrect Password"}), 400

@app.get('/users')
@role_required(['admin'])
def get_users():
    users = User.query.filter(User.roles.any(Role.name == 'store_manager')).all() 
    return marshal(users, user_fields)

@app.post('/store_manager_request/<int:id>/<string:action>')
@role_required(['admin'])
def store_manager_action(id, action):
    store_manager = User.query.filter_by(id=id).first() 
    if not store_manager:
        return jsonify({"message": "Store manager not found"}), 404
    
    if action not in ["approve", 'reject']:
        return jsonify({"message": "Invalid action"}), 400
    
    if action == 'approve':
        store_manager.active = True
        db.session.commit()
        return jsonify({"message": "Store manager approved"}), 200
    else:
        store_manager.is_rejected = True
        db.session.commit()
        return jsonify({"message": "Store manager rejected"}), 200

@app.get('/category_requests')
@role_required(['admin'])
def get_category_requests():
    category_requests = StoreManagerRequest.query.filter_by(is_rejected = False).all() 
    print(category_requests)
    return marshal(category_requests, category_request_fields)

@app.post('/category_request/<int:id>/<string:action>')
@role_required(['admin'])
def category_action(id, action):
    category_request = StoreManagerRequest.query.filter_by(id=id).first() 
    if not category_request:
        return jsonify({"message": "Category request not found"}), 404
    
    if action not in ["approve", 'reject']:
        return jsonify({"message": "Invalid action"}), 400
    
    if action == 'approve':
        if category_request.request == 'Create':
            category = Category(name=category_request.name, 
                                description=category_request.description, 
                                creator_id=category_request.creator_id)
            db.session.add(category)

        elif category_request.request == 'Edit':
            category = Category.query.filter_by(id=category_request.category_id).first()
            if category:
                category.name = category_request.name
                category.description = category_request.description
                for product in Product.query.filter_by(category_id=category.id).all():
                    product.category_name = category_request.name
        else:
            Category.query.filter_by(id=category_request.category_id).delete()

        category_request.is_approved = True
        db.session.commit()
        return jsonify({"message": "Category request approved"}), 200
    else:
        category_request.is_rejected = True
        db.session.commit()
        return jsonify({"message": "Category request rejected"}), 200
