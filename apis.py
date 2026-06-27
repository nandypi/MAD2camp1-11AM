from flask_restful import Api, Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_caching import Cache
from datetime import timedelta

api = Api()
cache = Cache()

from models import db, User, Item

## test resource

class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello! Greetings from the backend..."}
    def post(self):
        return {"message": "Post request received!"}
    def put(self):
        return {"message": "Put request received!"}
    def delete(self):
        return {"message": "Delete request received!"}
api.add_resource(HelloWorld, '/hello')

##

## auth resource

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        if not data or not data.get('email') or not data.get('password'):
            return {"message": "Please provide email and password!"}, 400
        user = User.query.filter_by(email=data['email']).first()
        if not user or user.password != data['password']:
            return {"message": "Invalid email or password!"}, 401
        access_token = create_access_token(user.email, expires_delta=timedelta(hours=1))
        return {"message": f"User {user.email} logged in successfully!", "token": access_token, "user": {"email": user.email, "role": user.role}}
api.add_resource(LoginResource, '/login')

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return {"message": "Please provide email and password!"}, 400
        if User.query.filter_by(email=data['email']).first():
            return {"message": "Email already exists!"}, 400
        user = User(email=data['email'], password=data['password'])
        db.session.add(user)
        db.session.commit()
        return {"message": f"User {user.email} registered successfully!"}, 201
api.add_resource(RegisterResource, '/register')

def IsAdmin() -> bool:
    request_user = User.query.filter_by(email=get_jwt_identity()).first()
    return request_user.role == "admin"

##
import time

class StatsResource(Resource):
    # @jwt_required()
    @cache.cached(timeout=30)
    def get(self):
        # if not IsAdmin():
        #     return {"message": "You are not allowed to do this"}, 403
        users_count = User.query.count()
        time.sleep(10) # Simulating a long-running operation
        items_count = Item.query.count()
        return {"message": "Stats returned successfully!", "stats": {"users_count": users_count, "items_count": items_count}}
api.add_resource(StatsResource, '/stats')

class CSVExportResource(Resource):
    # @jwt_required()
    def get(self):
        # if not IsAdmin():
        #     return {"message": "You are not allowed to do this"}, 403
        # Trigger the background task
        from celery_app import background_task
        background_task.delay()
        return {"message": "CSV export task has been triggered! You will receive an email once the task is completed."}
api.add_resource(CSVExportResource, '/export/csv')

## item resource

class ItemResource(Resource):
    @jwt_required()
    def get(self, item_id=None):
        if item_id:
            item = Item.query.get(item_id)
            if not item:
                return {"message": f"Item with id {item_id} not found!"}, 404
            return {"message": f"Item {item_id} returned!", "item": {"id": item.id, "name": item.name, "description": item.description, "image_url": item.image_url}}
        items = [{"id": item.id, "name": item.name, "description": item.description, "image_url": item.image_url} for item in Item.query.all()]
        return {"message": f"All items returned!", "items": items}
    @jwt_required()
    def post(self, item_id=None):
        if not IsAdmin():
            return {"message": "You are not allowed to do this"}, 403
        
        if item_id:
            return {"message": "Item id is not required for creation of new items!"}, 400
        data = request.get_json()
        if not data or not data.get('name'):
            return {"message": "Please provide required fields!"}, 400
        item = Item(name=data['name'], description=data.get('description'), image_url=data.get('image_url'))
        db.session.add(item)
        db.session.commit()
        return {"message": f"Item created successfully!", "item": {"id": item.id, "name": item.name, "description": item.description, "image_url": item.image_url}}, 201
    @jwt_required()
    def put(self, item_id):
        if not IsAdmin():
            return {"message": "You are not allowed to do this"}, 403

        item = Item.query.get(item_id)
        if not item:
            return {"message": f"Item with id {item_id} not found!"}, 404
        data = request.get_json()
        if not data or not data.get('name'):
            return {"message": "Please provide required fields!"}, 400
        item.name = data['name']
        item.description = data.get('description')
        item.image_url = data.get('image_url')
        db.session.commit()
        return {"message": f"Successfully updated item {item_id}!", "item": {"id": item.id, "name": item.name, "description": item.description, "image_url": item.image_url}}
    @jwt_required()
    def delete(self, item_id):
        if not IsAdmin():
            return {"message": "You are not allowed to do this"}, 403
        
        item = Item.query.get(item_id)
        if not item:
            return {"message": f"Item with id {item_id} not found!"}, 404
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Successfully deleted item {item_id}!"}
api.add_resource(ItemResource, '/items', '/items/<int:item_id>')

##