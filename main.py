from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# app definition
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

# env var for SQLAlchemy to handle postgres
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# customer data model
class Customer(db.Model):
  id = db.Column(db.Integer, primary_key=True) # auto-incremental
  name = db.Column(db.String(100), unique=True, nullable=False)
  dob = db.Column(db.Date)
  updated_at = db.Column(db.Date)

  def __init__(self, name, dob, updated_at):
    self.name = name
    self.dob = dob
    self.updated_at = updated_at

db.create_all() # SQLAlchemy create database table

# POST / CREATE
@app.route('/customers', methods=['POST'])
def add_customer():
  body = request.get_json()
  db.session.add(Customer(body['name'], body['dob']))
  db.session.commit()
  return "customer added"

# GET one / READ
@app.route('/customers/<id>', methods=['GET'])
def get_customer(id):
  customer = Customer.query.get(id)
  del customer.__dict__['_sa_instance_state']
  return jsonify(customer.__dict__)

# PUT / UPDATE
@app.route('/customers/<id>', methods=['PUT'])
def update_customer(id):
  body = request.get_json()
  db.session.query(Customer).filter_by(id=id).update(
    dict(name=body['name'], dob=body['dob']))
  db.session.commit()
  return "customer updated"

# DELETE
@app.route('/customers/<id>', methods=['DELETE'])
def delete_customer(id):
  db.session.query(Customer).filter_by(id=id).delete()
  db.session.commit()
  return "customer deleted"

# GET all / LIST
@app.route('/customers', methods=['GET'])
def get_customers():
  customers = []
  for customer in db.session.query(Customer).all():
    del customer.__dict__['_sa_instance_state']
    customers.append(customer.__dict__)
  return jsonify(customers)
