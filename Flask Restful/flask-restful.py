from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app) # This will connect Flask-RESTful to the app we created one the line before

contacts = {} # This is just a dummy/mini database

class Contact(Resource):
    def post(self, contact_id):
        data = request.get_json()  # expects JSON input
        contacts[contact_id] = data
        return f"Your Data Is Saved: {data}"


api.add_resource(Contact, '/contact/<string:contact_id>')

if __name__ == '__main__':
    app.run(debug=True,port=5008)
