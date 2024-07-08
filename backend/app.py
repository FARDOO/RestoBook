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
    
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        name = data.get('name')
        password = data.get('password')      

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
        email = data.get('email')
        
        customer_name = Customer.query.filter_by(name=name).first()
        customer_email = Customer.query.filter_by(email=email).first()
        if not name:
            return jsonify({'message' : 'error request'})   
          
        if customer_name:
            
            if customer_email:
                return jsonify({'id': '',
                                'name': '',
                                'email': '',
                                'name_exists': 'true',
                                'email_exists': 'true'}) 
            return jsonify({'id': '',
                                'name': '',
                                'email': '',
                                'name_exists': 'true',
                                'email_exists': 'false'}) 
        else:
            if customer_email:
                return jsonify({'id': '',
                                'name': '',
                                'email': '',
                                'name_exists': 'false',
                                'email_exists': 'true'})        
        

        new_customer = Customer(name = name, password = password, email=email)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'customer': {'id': new_customer.id,
                                     'name' : new_customer.name,
                                     'email' : new_customer.email,
                                     'name_exists': 'false',
                                     'email_exists': 'false'}}), 201
    except Exception as error:
        print("error: ", error)
        return jsonify({'message' : 'server error'}), 500     
    
"""
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
"""        
    
"""
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
"""

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

            'image_url' : restaurant.image_url
        }     
 
            

        return jsonify(restaurant_data), 201
    except Exception as error:
        return jsonify({'message' : 'server error'}), 500     
         

@app.route('/reservations', methods=['GET'])
def get_reservations():
    try:
        reservations = Reservation.query.all()
        reservations_data = []
        for reservation in reservations:
            reservation_data = {
                'id' : reservation.id,
                'customer_id' : reservation.customer_id,
                'restaurant_id' : reservation.restaurant_id,
                'diners' : reservation.diners,
                'date' : reservation.date,
                'time_of_day' : reservation.time_of_day,
            }
            reservations_data.append(reservation_data)
        return jsonify(reservations_data), 201
    except Exception as error:
        return jsonify({'message' : 'server error'}), 500 


@app.route('/reservation', methods=['POST'])
def add_reservation():
    try:
        data = request.json
        customer_name = data.get('customer_name')
        restaurant_id = data.get('restaurant_id')
        diners = int(data.get('diners'))
        date = data.get('date')
        time_of_day = data.get('time_of_day')

        restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
        if not restaurant:
            print("1")
            return jsonify({'message': 'Restaurante no encontrado'}), 404
        
        customer = Customer.query.filter_by(name=customer_name).first()
        if not customer:
            print("2")
            return jsonify({'message': 'Cliente no resgistrado, por favor registrese'}), 404
        
        customer_id = customer.id

        if not all([customer_id, restaurant_id, diners, date, time_of_day]):
            print("3")
            return jsonify({'message' : 'error request'}), 400
        print("A")
        capacity = restaurant.capacity
        print("B")
        reservations = Reservation.query.filter_by(restaurant_id=restaurant_id, date=date).all()
        print("C")
        total_diners = sum(reservation.diners for reservation in reservations)
        print("D")
        if total_diners + int(diners) > capacity:
            return jsonify({'message': 'Capacidad máxima excedida para este restaurante y fecha'}), 400
        elif time_of_day == 'lunch' and not restaurant.lunch:
            return jsonify({'message': 'Este restaurante no sirve almuerzo'}), 400
        elif time_of_day == 'dinner' and not restaurant.dinner:
            return jsonify({'message': 'Este restaurante no sirve cena'}), 400
        print("E")
        new_reservation = Reservation(customer_id = customer_id, restaurant_id = restaurant_id,
                                      diners = diners, date = date, time_of_day = time_of_day)
        print("F")
        db.session.add(new_reservation)
        print("G")
        db.session.commit()
        print("H")

        return jsonify({
            'message': 'Reserva creada exitosamente',
        }), 201
    
    except Exception as error:
        print("error: ", error)
        return jsonify({'message' : 'server error'}), 500     


if __name__ == '__main__':
    print('Starting Server...')
    db.init_app(app)
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Started...')

