"""Flask app for Cupcakes"""

from flask import Flask, render_template, redirect, jsonify, request
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] =True
app.config['SECRET_KEY'] = 'shhh-secret'

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
  '''Homepage'''
  return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
  'Listing all the cupcakes.'
  cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
  return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
  'Create a cupcake.'
  cupcake = Cupcake(
    flavor = request.json['flavor'],
    size = request.json['size'],
    rating = request.json['rating'],
    image = request.json['image'] or None
  )
  db.session.add(cupcake)
  db.session.commit()
  return jsonify(cupcake=cupcake.serialize()), 201

@app.route('/api/cupcakes/<int:cupcake_id>')
def list_cupcake(cupcake_id):
  '''Listing a single cupcake'''

  cupcake = Cupcake.query.get_or_404(cupcake_id)
  return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def edit_cupcake(cupcake_id):
  '''Editing a cupcake'''

  cupcake = Cupcake.query.get_or_404(cupcake_id)

  cupcake.flavor = request.json['flavor']
  cupcake.size = request.json['size']
  cupcake.rating = request.json['rating']
  cupcake.image = request.json['image']

  db.session.add(cupcake)
  db.session.commit()
  return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
  '''Deleting a cupcake'''

  cupcake = Cupcake.query.get_or_404(cupcake_id)

  db.session.delete(cupcake)
  db.session.commit()
  return jsonify(message="Deleted")
