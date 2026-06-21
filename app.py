from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello():
    if request.method == 'GET':
        return {"message": "Get request received!"}
    elif request.method == 'POST':
        return {"message": "Post request received!"}
    elif request.method == 'PUT':
        return {"message": "Put request received!"}
    elif request.method == 'DELETE':
        return {"message": "Delete request received!"}
    # return render_template('index.html') # returning a template instead of data
    return {"message": "Hello, World!"} # returning data as JSON response

api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"message": "Get request received!"}
    def post(self):
        return {"message": "Post request received!"}
    def put(self):
        return {"message": "Put request received!"}
    def delete(self):
        return {"message": "Delete request received!"}

api.add_resource(HelloWorld, '/bye')

if __name__ == '__main__':
    app.run(debug=True)