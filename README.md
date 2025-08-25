<h1>
  RestoBook - Restaurant Reservation System
</h1>
<div align="center">
    <img src="https://t4.ftcdn.net/jpg/02/94/26/33/360_F_294263329_1IgvqNgDbhmQNgDxkhlW433uOFuIDar4.jpg" title="Restaurant Image"
       style="width: 60vw; height: auto;" />
</div>
 <h2> Content: </h2>

- Description
- Features
- Technologies Used
- Team Members
- Database Structure
- Endpoints
- Addresses

<h2> Description </h2>

Resto Book is a web application designed to facilitate table reservations at various restaurants in the city. Users can sign up, log in, view a list of restaurants, and make, update, or cancel reservations.

<h2> Characteristics:</h2>

- Registration of new customers.
- Customer login.
- Viewing a list of restaurants.
- Making reservations at restaurants.
- Updating and canceling existing reservations.
- Validations for capacity and service availability (lunch/dinner).

<h2> Technologies Used </h2>

1. Backend: Flask, SQLAlchemy
2. Frontend: Framework Bootstrap
3. DataBase: PostgreSQL

<h2> Team Members:</h2>

- Condori Hector 
- Santiago Fardini

<h2> Database Structure: </h2>
  
  The Database is composed of three tables:

- Restaurant:
  - id (Primary Key)
  - name (Name of the Restaurant)
  - capacity (Maximum capacity per day)
  - dinner (True if available for dinner)
  - lunch (True if available for lunch)
  - image_url (URL address of the Restaurant's image)

- Customer:
  - id (Primary Key)
  - name (Name of the customer)
  - password (Customer's password)
  - email (Customer's email)
  - reservation_list (table relationship)

- Reservation:
  - id (Primary Key)
  - customer_id (Customer's Foreign Key)
  - restaurant_id (Restaurant's Foreign Key)
  - diners (Number of people in the reservation)
  - date (Reservation date)
  - time_of_day (Whether it's for dinner or lunch)

<h2> Endpoints: </h2>

1. Customers
    - GET /customers: Get the list of customers.
    - POST /login: Log in.
    - POST /customer: Register a new customer.

2. Restaurants
    - GET /restaurants: Get the list of restaurants.
    - GET /restaurants/<id>: Get a restaurant by its ID.

3. Reservations
    - POST /reservation: Create a new reservation.
    - GET /reservation/<id>: Get a reservation by its ID.
    - GET /reservations/<customer_id>: Get reservations by customer ID.
    - GET /reservations: Get all reservations.
    - PUT /updatereservation/<id>: Update a reservation.
    - DELETE /deletereservation/<id>: Delete a reservation.
  
<h2> Addresses: </h2>

- Home (Shows the list of all Restaurants):
  "/"
- Restaurant (Shows information of the selected Restaurant):
  "/restaurant/?id="id"&name="name""
- Make Reservation (Form to make a reservation at the previously selected Restaurant):
  "/createreservation/?id="id"&name="name""
- View My Reservations (View reservations under our name):
  "/myreservations/"
- Update Reservation (Update the selected reservation):
  "/updatereservation/?id="id""
- Log in (Allows user to log in):
  "/login/"
- Register (Allows user to create an account):
  "/register/"


