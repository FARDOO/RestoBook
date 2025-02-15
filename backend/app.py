# app.py
from flask import jsonify
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Restaurant, Reservation, Customer  
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
        return jsonify({'message' : 'estoy en customers'}),200
    except Exception as error:
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
        data = request.json
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
       
         
@app.route('/updatereservation/<id>', methods=['PUT'])
def update_reservation(id):
    data = request.get_json()  
    reservation = Reservation.query.get(id)  
    try:
       
        restaurant_id = reservation.restaurant_id 
        restaurant = Restaurant.query.filter_by(id=restaurant_id).first()


        diners = int(data.get('diners'))
        date = data.get('date')
        capacity = restaurant.capacity
        
        reservations = Reservation.query.filter_by(restaurant_id=restaurant_id, date=data['date']).all()
       
        total_diners = sum(reservation.diners for reservation in reservations)
        if str(reservation.date) == str(date):
            total_diners = total_diners - reservation.diners

        if total_diners + int(diners) > capacity:
            return jsonify({'message': 'Capacidad máxima excedida para este restaurante y fecha', 'exitoso': False }), 400
        elif data['time_of_day'] == 'lunch' and not restaurant.lunch:
            return jsonify({'message': 'Este restaurante no sirve almuerzo', 'exitoso': False}), 400
        elif data['time_of_day'] == 'dinner' and not restaurant.dinner:
            return jsonify({'message': 'Este restaurante no sirve cena', 'exitoso': False}), 400
        
        reservation.date = data['date']
        reservation.diners = data['diners']
        reservation.time_of_day = data['time_of_day']

        db.session.commit() 
        return jsonify({'message': 'Reserva actualizada con exito', 'exitoso': True}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'server error', 'exitoso': False}), 500 


@app.route('/reservation/<id>', methods=['GET'])
def get_reservation_by_id(id):
    try:
        reservation = Reservation.query.get(id)
        restaurant_id = reservation.restaurant_id
        restaurant = Restaurant.query.get(restaurant_id)

        reservation_data = {
            'id' : reservation.id,
            'customer_id' : reservation.customer_id,
            'restaurant_id' : restaurant_id,
            'restaurant_name' : restaurant.name,
            'diners' : reservation.diners,
            'date' : reservation.date.strftime('%Y-%m-%d'),
            'time_of_day' : reservation.time_of_day,
        }     
        return jsonify(reservation_data), 201
    except Exception as error:
        return jsonify({'message' : 'server error'}), 500   
    

@app.route('/reservations/<customer_id>', methods=['GET'])
def get_reservations_for_customer_id(customer_id):
    try:
        reservations = Reservation.query.filter_by(customer_id=customer_id).order_by(Reservation.date.asc()).all()
        reservations_data = []

        if not reservations:
            return jsonify(reservations_data), 201   
           
        for reservation in reservations:
            restaurant = Restaurant.query.get(reservation.restaurant_id) 
            reservation_data = {
                'id' : reservation.id,
                'customer_id' : reservation.customer_id,
                'restaurant_id' : reservation.restaurant_id,
                'restaurant_name' : restaurant.name,
                'diners' : reservation.diners,
                'date' : reservation.date.strftime('%Y-%m-%d'),
                'time_of_day' : reservation.time_of_day,
            }
            reservations_data.append(reservation_data)
        return jsonify(reservations_data), 201
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
            return jsonify({'message': 'Restaurante no encontrado', 'exitoso': True}), 404
        
        customer = Customer.query.filter_by(name=customer_name).first()
        if not customer:
            return jsonify({'message': 'Cliente no resgistrado, por favor registrese', 'exitoso': True}), 404
        
        customer_id = customer.id

        if not all([customer_id, restaurant_id, diners, date, time_of_day]):
            return jsonify({'message' : 'error request'}), 400
        capacity = restaurant.capacity
        reservations = Reservation.query.filter_by(restaurant_id=restaurant_id, date=date).all()
        total_diners = sum(reservation.diners for reservation in reservations)
        if total_diners + int(diners) > capacity:
            return jsonify({'message': 'Capacidad máxima excedida para este restaurante y fecha', 'exitoso': False}), 400
        elif time_of_day == 'lunch' and not restaurant.lunch:
            return jsonify({'message': 'Este restaurante no sirve almuerzo', 'exitoso': False}), 400
        elif time_of_day == 'dinner' and not restaurant.dinner:
            return jsonify({'message': 'Este restaurante no sirve cena', 'exitoso': False}), 400
        new_reservation = Reservation(customer_id = customer_id, restaurant_id = restaurant_id,
                                      diners = diners, date = date, time_of_day = time_of_day)
        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({
            'message': 'Reserva creada exitosamente', 'exitoso': True
        }), 201
    
    except Exception as error:
        print("error: ", error)
        return jsonify({'message' : 'server error', 'exitoso': False}), 500     


@app.route('/deletereservation/<id>', methods=['DELETE'])
def delete_reservation(id):
    reservation = Reservation.query.get(id)

    if not reservation:
        return jsonify({'message': 'No existe reservacion'}), 201
    
    try:
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({'message': 'reservacion borrada'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'error'}), 500


if __name__ == '__main__':
    print('Starting Server...')
    db.init_app(app)
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Started...')

