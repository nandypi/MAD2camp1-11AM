from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'your-secret-key' # you can keep it in .env and load it using python-dotenv for better security
jwt = JWTManager(app)

# connecting to the database
from models import db, User
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# connecting to the API
from apis import api, cache
api.init_app(app)
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache.init_app(app)

## This is the old way of handling routes without using Flask-RESTful; mad1 and mad2 are two different ways of returning responses (template vs JSON); we will be using the JSON response method for our API development, so we will comment out this route handler and use the one defined in apis.py instead.
# @app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def hello():
#     if request.method == 'GET':
#         return {"message": "Get request received!"}
#     elif request.method == 'POST':
#         return {"message": "Post request received!"}
#     elif request.method == 'PUT':
#         return {"message": "Put request received!"}
#     elif request.method == 'DELETE':
#         return {"message": "Delete request received!"}
#     # return render_template('index.html') # returning a template instead of data; mad1
#     return {"message": "Hello, World!"} # returning data as JSON response; mad2

if __name__ == '__main__':

    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist

        # Check if an admin user already exists; if not, create one
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(role='admin', email='admin@gmail.com', password='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created with email: admin@gmail.com and password: admin")
        else:
            print("Admin user already exists with email: admin@gmail.com and password: admin")

    app.run(debug=True)