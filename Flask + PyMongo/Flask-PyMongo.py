from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client["zaid"]
collection = db["contacts"]
score_collection = db["scores"]

@app.route('/add',methods=["POST","GET"])
def add():
    if request.method == "GET":
        return '''
        <h2>Add Contact</h2>
        <form method="POST">
            Name: <input type="text" name="name"><br><br>
            Phone: <input type="text" name="phone"><br><br>
            Email: <input type="text" name="email"><br><br>
            <input type="submit" value="Add Contact">
        </form>
        '''
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    collection.insert_one({
        "name": name,
        "phone": phone,
        "email": email
    })
    return f"{name}'s Contact Is Added!" 

@app.route('/users', methods=['GET'])
def get_users():
    users = collection.find({},{'_id':0})
    return jsonify(list(users))

@app.route('/find/<id>')
def find(id):
    query = collection.find_one({'_id':ObjectId(id)},{'_id':0,'name':1,'phone':1,'email':1})
    if query:
        return jsonify(query)
    return 'User Not Found!'

@app.route('/bulk', methods=['GET'])
def bulk_insert():
    data = [
        {"name": "Marques", "phone": "008-845-9931", "email": "marques@yahoo.com"},
        {"name": "Sabastian", "phone": "886-925-1726", "email": "sabastian@yahoo.com"},
        {"name": "Tommy", "phone": "996-843-8836", "email": "tommy@gmail.com"}
    ]
    collection.insert_many(data)
    return "Bulk Insert Done!"


@app.route('/score/above/<int:min_score>')
def score_above(min_score):
    result = score_collection.find({"score": {"$gte": min_score}}, {'_id': 0})
    return jsonify(list(result))

@app.route('/score/below/<int:max_score>')
def score_below(max_score):
    result = score_collection.find({"score": {"$lte": max_score}}, {'_id': 0})
    return jsonify(list(result))

@app.route('/score/between/<int:min_score>/<int:max_score>')
def score_between(min_score,max_score):
    result = score_collection.find({"score": {"$lte": max_score,"$gte": min_score}}, {'_id': 0})
    return jsonify(list(result))

# @app.route('/addscoredata')
# def add_score_data():
#     data = [
#         {"name": "Eric", "score": 70},
#         {"name": "Sabastian", "score": 85},
#         {"name": "Tommy", "score": 40},
#         {"name": "Nemesis", "score": 95},
#     ]
#     score_collection.insert_many(data)
#     return "Sample score data added!"

if __name__ == '__main__':
    app.run(debug=True,port=5009)