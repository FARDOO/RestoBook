# app.py
from flask import jsonify
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Restaurant, Reservation, Customer  # Asegúrate de importar db correctamente

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://santiago:1234@localhost:5432/restobook_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    
@app.route('/customer', methods=['POST'])
def add_customer():
    try:
        print("estoy en post")
        data = request.json
        name = data.get('name')
        if not name:
            return jsonify({'message' : 'error request'})
        new_customer = Customer(name = name)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'customer': {'id': new_customer.id,
                                     'name' : new_customer.name}}), 201
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
    