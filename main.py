import logging
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import datetime
import jwt

# logging.getLogger().setLevel(logging.INFO)

# app definition
app = Flask(__name__)

# env variables
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

# admin data model
class Admin(db.Model):
  id = db.Column(db.Integer, primary_key=True) # auto-incremental
  name = db.Column(db.String(50))
  password = db.Column(db.String(100))

  def __init__(self, name, password):
    self.name = name
    self.password = password

# customer data model
class Customer(db.Model):
  id = db.Column(db.Integer, primary_key=True) # auto-incremental
  name = db.Column(db.String(100))
  dob = db.Column(db.Date)
  updated_at = db.Column(db.Date)

  def __init__(self, name, dob, updated_at):
    self.name = name
    self.dob = dob
    self.updated_at = updated_at

db.create_all() # SQLAlchemy create database table

@app.route("/")
def main():
  return "Klinify Engineer Task - Ariff Azman"

# POST / CREATE
@app.route('/api/v1/admins', methods=['POST'])
def add_admin():
  data = request.get_json()
  hashedPassword = generate_password_hash(data['password'], method='sha256')
  db.session.add(Admin(data['name'], hashedPassword))
  db.session.commit()
  return jsonify({'message': 'admin added'})

# GET all / LIST all
@app.route('/api/v1/admins/all', methods=['GET'])
def get_admins():
  admins = []
  for admin in db.session.query(Admin).all():
    del admin.__dict__['_sa_instance_state']
    admins.append(admin.__dict__)
  return jsonify(admins)

# POST / CREATE
@app.route('/api/v1/customers', methods=['POST'])
def add_customer():
  data = request.get_json()
  db.session.add(Customer(data['name'], data['dob'], datetime.datetime.now()))
  db.session.commit()
  return jsonify({'message': 'customer added'})

# GET one / READ
# .../api/v1/customers?id=1
@app.route('/api/v1/customers', methods=['GET'])
def get_customer():
  if not 'id' in request.args:
    return jsonify({'message': 'provide customer id'})

  customer = Customer.query.get(int(request.args['id']))
  if not customer:
    return jsonify({'message': 'customer not found'})
  del customer.__dict__['_sa_instance_state']
  return jsonify(customer.__dict__)

# PUT / UPDATE
@app.route('/api/v1/customers', methods=['PUT'])
def update_customer():
  if not 'id' in request.args:
    return jsonify({'message': 'provide customer id'})

  customer = Customer.query.get(int(request.args['id']))
  if not customer:
    return jsonify({'message': 'customer not found'})

  data = request.get_json()
  db.session.query(Customer).filter_by(id=int(request.args['id'])).update(
    dict(name=data['name'], dob=data['dob'], updated_at=datetime.datetime.now()))
  db.session.commit()
  return jsonify({'message': 'customer updated'})


# DELETE
@app.route('/api/v1/customers', methods=['DELETE'])
def delete_customer():
  if not 'id' in request.args:
    return jsonify({'message': 'provide customer id'})

  customer = Customer.query.get(int(request.args['id']))
  if not customer:
    return jsonify({'message': 'customer not found'})

  db.session.query(Customer).filter_by(id=int(request.args['id'])).delete()
  db.session.commit()
  return jsonify({'message': 'customer deleted'})

# GET all / LIST all
@app.route('/api/v1/customers/all', methods=['GET'])
def get_customers():
  customers = []
  for customer in db.session.query(Customer).all():
    # logging.info(customer.__dict__['_sa_instance_state'])
    del customer.__dict__['_sa_instance_state']
    customers.append(customer.__dict__)
  return jsonify(customers)

# GET youngest / LIST youngest
@app.route('/api/v1/customers/youngest/<size>', methods=['GET'])
def get_customers_youngest(size):
  customers = []
  for customer in db.session.query(Customer).order_by(Customer.dob.desc()).limit(size):
    del customer.__dict__['_sa_instance_state']
    customers.append(customer.__dict__)
  return jsonify(customers)

# GET oldest / LIST oldest
@app.route('/api/v1/customers/oldest/<size>', methods=['GET'])
def get_customers_oldest(size):
  customers = []
  for customer in db.session.query(Customer).order_by(Customer.dob.asc()).limit(size):
    del customer.__dict__['_sa_instance_state']
    customers.append(customer.__dict__)
  return jsonify(customers)


@app.route('/api/v1/admins/login')
def login():
  auth = request.authorization

  if not auth or not auth.username or not auth.password:
    return make_response('Invalid login', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

  user = db.session.query(Admin).filter_by(name=auth.username).first()

  if not user:
    return make_response('Invalid login', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

  if not check_password_hash(user.password, auth.password):
    return make_response('Invalid login', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

  token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'])
  return jsonify({'token': token})


if __name__ == '__main__':
    app.run(debug=True)
