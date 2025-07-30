from flask import Flask,render_template,request
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
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.customer_id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

class Customer(db.Model):
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


@app.route('/')
def Home():
    return 'Hello, This is home page!'

@app.route('/orders')
def orders():
    orders = Order.query.all()
    all_orders = []
    for x in orders:
        all_orders.append({
            'order_id': x.order_id,
            'customer_id': x.customer_id,
            'order_date': x.order_date,
            'total_amount': x.total_amount,
            'status': x.status
        })
    return all_orders

@app.route('/customers')
def customers():
    users = Customer.query.all()
    all_users = []
    for x in users:
        all_users.append({
            'customer_id': x.customer_id,
            'first_name': x.first_name,
            'last_name': x.last_name,
            'email': x.email,
            'phone': x.phone,
            'created_at' : x.created_at
        })
    return all_users

@app.route('/add_customer', methods=['POST','GET'])
def add_customer():
    if request.method == "GET":
        return render_template('add_customer.html')
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    new_customer = Customer(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        created_at=datetime.now()
    )
    db.session.add(new_customer)
    db.session.commit()
    return f"Customer {first_name} added successfully!"

@app.route('/add_order', methods=['POST','GET'])
def add_order():
    if request.method == "GET":
        return render_template('add_order.html')
    customer_id = request.form['customer_id']
    order_date = datetime.now()
    total_amount = request.form['total_amount']
    status = request.form['status']
    new_order = Order(
        customer_id=customer_id,
        order_date=order_date,
        total_amount=total_amount,
        status=status
    )
    db.session.add(new_order)
    db.session.commit()
    return f"Order added successfully!"


@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    user = Customer.query.get_or_404(id)
    if request.method == "POST":
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        db.session.commit()
        return f"Customer {user.first_name} updated successfully!"
    return render_template('edit_customer.html',user=user)

@app.route('/edit_order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    order = Order.query.get_or_404(id)
    if request.method == "POST":
        order.order_id = request.form['order_id']
        order.customer_id = request.form['customer_id']
        order.order_date = request.form['order_date']
        order.total_amount = request.form['total_amount']
        order.status = request.form['status']
        db.session.commit()
        return f"Order {order.order_id} updated successfully!"
    return render_template('edit_order.html',order=order)

@app.route('/delete_customer/<int:id>', methods=['GET'])
def delete_customer(id):
    user = Customer.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return f"Customer {user.first_name} deleted successfully!"

@app.route('/delete_order/<int:id>', methods=['GET'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return f"Order {order.order_id} deleted successfully!"

if __name__ == '__main__':
    app.run(port=5002,debug=True)