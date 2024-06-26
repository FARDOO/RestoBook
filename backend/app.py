# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Restaurant, Reservation, Customer  # Asegúrate de importar db correctamente

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://santiago:1234@localhost:5432/prueba'
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

if __name__ == '__main__':
    print('Starting Server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Started...')
