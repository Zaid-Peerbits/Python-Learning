from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Connection URI format:
# 'mysql+pymysql://username:password@host/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://zaid:0000@localhost/mytest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # this is optional and will only increase performance of app

db = SQLAlchemy(app)

class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

class Customers(db.Model):
    __tablename__ = 'Customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


with app.app_context():
    db.create_all()
    print(db.inspect(db.engine).get_table_names())

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # this are columns to be added to table
#     name = db.Column(db.String(50))


@app.route('/')
def Home():
    return 'Hello, This is home page!'






if __name__ == '__main__':
    app.run(port=5007,debug=True)