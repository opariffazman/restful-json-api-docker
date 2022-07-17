from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
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

db.create_all() # SQLAlchemy create database tables

# START JWT Auth  ======================================================================

# admin auth for JWT
@app.route('/api/v1/admins/auth')
def adminToken():
  auth = request.authorization

  if not auth or not auth.username or not auth.password:
    return make_response('Invalid login', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

  user = db.session.query(Admin).filter_by(name=auth.username).first()

  if not user:
    return make_response('Invalid login', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

  if not check_password_hash(user.password, auth.password):
    return make_response('Invalid login', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

  token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)}, app.config['SECRET_KEY'])
  return jsonify({'token': token})

def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' not in request.headers:
            return jsonify({'message' : 'Token is missing!'}), 401

        token = request.headers['x-access-token']

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            adminAuthenticated = db.session.query(Admin).filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(adminAuthenticated, *args, **kwargs)

    return decorated

# END JWT Auth ========================================================================

@app.route("/")
def main():
  return "Klinify Engineer Task - Ariff Azman"

# START ADMIN ROUTES ==================================================================

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
@tokenRequired
def get_admins(adminAuthenticated):
  if not adminAuthenticated:
    return jsonify({'message': 'unauthorized'})

  admins = []
  for admin in db.session.query(Admin).all():
    del admin.__dict__['_sa_instance_state']
    admins.append(admin.__dict__)
  return jsonify(admins)

# END ADMIN ROUTES ==================================================================

# START CUSTOMER ROUTES =============================================================

# POST / CREATE
@app.route('/api/v1/customers', methods=['POST'])
@tokenRequired
def add_customer(adminAuthenticated):
  if not adminAuthenticated:
    return jsonify({'message': 'unauthorized'})

  data = request.get_json()
  db.session.add(Customer(data['name'], data['dob'], datetime.datetime.now()))
  db.session.commit()
  return jsonify({'message': 'customer added'})

# GET one / READ
# .../api/v1/customers?id=1
@app.route('/api/v1/customer', methods=['GET'])
@tokenRequired
def get_customer(adminAuthenticated):
  if not adminAuthenticated:
    return jsonify({'message': 'unauthorized'})

  if not 'id' in request.args:
    return jsonify({'message': 'provide customer id'})

  customer = Customer.query.get(int(request.args['id']))
  if not customer:
    return jsonify({'message': 'customer not found'})
  del customer.__dict__['_sa_instance_state']
  return jsonify(customer.__dict__)

# PUT / UPDATE
@app.route('/api/v1/customer', methods=['PUT'])
@tokenRequired
def update_customer(adminAuthenticated):
  if not adminAuthenticated:
    return jsonify({'message': 'unauthorized'})

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
@app.route('/api/v1/customer', methods=['DELETE'])
@tokenRequired
def delete_customer(adminAuthenticated):
  if not adminAuthenticated:
    return jsonify({'message': 'unauthorized'})

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
@tokenRequired
def get_customers(adminAuthenticated):
  if not adminAuthenticated:
    return jsonify({'message': 'unauthorized'})

  customers = []
  for customer in db.session.query(Customer).all():
    del customer.__dict__['_sa_instance_state']
    customers.append(customer.__dict__)
  return jsonify(customers)

# GET size / LIST size
# .../api/v1/customers?size=1
@app.route('/api/v1/customers', methods=['GET'])
@tokenRequired
def get_customers_size(adminAuthenticated):
  if not adminAuthenticated:
    return jsonify({'message': 'unauthorized'})

  if not 'size' in request.args:
    return jsonify({'message': 'provide customer size'})

  customers = []
  for customer in db.session.query(Customer).order_by(Customer.dob.desc()).limit(int(request.args['size'])):
    del customer.__dict__['_sa_instance_state']
    customers.append(customer.__dict__)
  return jsonify(customers)

# END CUSTOMER ROUTES ===============================================================

if __name__ == '__main__':
    app.run(debug=True)
