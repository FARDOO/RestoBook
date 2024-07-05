# app.py
from flask import jsonify
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Restaurant, Reservation, Customer  # Asegúrate de importar db correctamente
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://santiago:1234@localhost:5432/restobook_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()

CORS(app)
@app.route("/")
def home():
    return """
    <html>
    <body>
    <h1>Welcome to Resto Book</h1> 
    <a href="/restaurants">Go to all restaurants</a>
    <a href="/reservations">Go to my reservations</a>
    </body>
    </html>
    """

@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        print("estoy en customers")
        return jsonify({'message' : 'estoy en customers'}),200
    except Exception as error:
        print("error: ", error)
        return jsonify({'message': 'server error'}), 500
    
@app.route('/login', methods=['GET'])
def login():
    try:
        name = request.args.get('name')
        print(name)
        password = request.args.get('password')
        print(password)
        customer = Customer.query.filter_by(name=name).first()
        if not customer:
            return jsonify({'id': '',
                            'name': '',
                            'login_u': 'false',
                            'login_p': 'false'})        
  
        if customer and customer.password != password:
            return jsonify({'id': '',
                            'name': '',
                            'login_u': 'true',
                            'login_p': 'false'}) 
        
        customer_data = {
                'id' : customer.id,
                'name' : customer.name,
                'login_u' : "true",
                'login_p' : "true"
        }        
        return jsonify(customer_data),201
    except Exception as error:        
        return jsonify({'message': 'server error'}), 500
    
@app.route('/customer', methods=['POST'])
def add_customer():
    try:       
        print(request.json)        
        data = request.json
        print(request.json)
        name = data.get('name')
        password = data.get('password')
        
        if not name:
            return jsonify({'message' : 'error request'})
        new_customer = Customer(name = name, password = password)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'customer': {'id': new_customer.id,
                                     'name' : new_customer.name}}), 201
    except Exception as error:
        print("error: ", error)
        return jsonify({'message' : 'server error'}), 500     
    

@app.route('/customer/validation/<name>', methods=['GET'])
def name_exists(name):
    try:
        customer = Customer.query.filter_by(name=name).first()
        if not customer:
            return jsonify({'exists': 'false'})        
        else:
            return jsonify({'exists': 'true'}) 
        
    except Exception as error:
        print("error: ", error)
        return jsonify({'message' : 'server error'}), 500

@app.route('/customer/validation/<email>', methods=['GET'])
def email_exists(email):
    try:
        customer = Customer.query.filter_by(email=email).first()
        if not customer:
            return jsonify({'exists': 'false'})        
        else:
            return jsonify({'exists': 'true'}) 
        
    except Exception as error:
        print("error: ", error)
        return jsonify({'message' : 'server error'}), 500        

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        restaurants = Restaurant.query.all()
        restaurants_data = []
        for restaurant in restaurants:
            restaurant_data = {
                'id' : restaurant.id,
                'name' : restaurant.name,
                'capacity' : restaurant.capacity,
                'dinner' : restaurant.dinner,
                'lunch' : restaurant.lunch,
                'image_url' : restaurant.image_url
            }
            restaurants_data.append(restaurant_data)
        return jsonify(restaurants_data), 201
    except Exception as error:
        return jsonify({'message' : 'server error'}), 500 

@app.route('/restaurants/<id>', methods=['GET'])
def get_restaurant_by_id(id):
    try:
        restaurant = Restaurant.query.get(id)       
        restaurant_data = {
            'id' : restaurant.id,
            'name' : restaurant.name,
            'capacity' : restaurant.capacity,
            'dinner' : restaurant.dinner,
            'lunch' : restaurant.lunch,
            'image_url' : restaurant.image_url        }   
            
        return jsonify(restaurant_data), 201
    except Exception as error:
        return jsonify({'message' : 'server error'}), 500          

if __name__ == '__main__':
    print('Starting Server...')
    db.init_app(app)
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Started...')

