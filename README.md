<h1>
  Resto Book - Sistema de Reservas en Restaurantes
</h1>

 <h2> Contenido: </h2>

- Descripcion
- Caracteristicas
- Tecnologias Utilizadas
- Integrantes
- Estructura de la Base de Datos
- Endpoints
- Direcciones

<h2> Descripcion </h2>

Resto Book es una aplicación web diseñada para facilitar la reserva de mesas en diversos restaurantes de la ciudad. Los usuarios pueden registrarse, iniciar sesión, ver una lista de restaurantes, y realizar, actualizar o cancelar reservas.

<h2> Caracteristicas:</h2>

- Registro de nuevos clientes.
- Inicio de sesión de clientes.
- Visualización de una lista de restaurantes.
- Realización de reservas en restaurantes.
- Actualización y cancelación de reservas existentes.
- Validaciones de capacidad y disponibilidad de servicios (almuerzo/cena).

<h2> Tecnologias Utilizadas </h2>

1. Backend: Flask, SQLAlchemy
2. Frontend: Framework Bootstrap
3. Base de Datos: PostgreSQL

<h2> Integrantes:</h2>

- Condori Hector 
- Santiago Fardini

<h2> Estructura de la Base de Datos: </h2>
  
  La Base de Datos esta conformada por tres tablas: 

  - Restaurant: id (Primary Key)
                name (Nombre del Restaurant)
                capacity (Capacidad maxima por dia)
                dinner (True si esta disponible para cenar)
                lunch (True si esta disponible para almorzar)
                image_url (Direccion URL de la imagen del Restaurant)

  - Customer: id (Primary Key)
              name (Nombre del cliente)
              password (Constraseña del cliente)
              email (mail del cliente)
              reservation_list (relacion entre tablas)

  - Reservation: id (Primary Key)
                 customer_id (Foreign Key del cliente)
                 restaurant_id (Foreign Key del restaurant)
                 diners (Cantidad de personas en la reserva)
                 date (Fecha de la reserva)
                 time_of_day(Si es para cenar o almorzar)

<h2> Endpoints: </h2>

1. Clientes
    - GET /customers: Obtener la lista de clientes.
    - POST /login: Iniciar sesión.
    - POST /customer: Registrar un nuevo cliente.

2. Restaurantes
    - GET /restaurants: Obtener la lista de restaurantes.
    - GET /restaurants/<id>: Obtener un restaurante por su ID.

3. Reservas
    - POST /reservation: Crear una nueva reserva.
    - GET /reservation/<id>: Obtener una reserva por su ID.
    - GET /reservations/<customer_id>: Obtener reservas por ID de cliente.
    - GET /reservations: Obtener todas las reservas.
    - PUT /updatereservation/<id>: Actualizar una reserva.
    - DELETE /deletereservation/<id>: Eliminar una reserva.

<h2> Direcciones: </h2>

- Inicio (Me muestra el listado de todos los Restaurants): "/"
- Restaurant (Me muestra informacion del Restaurant seleccionado): "/restauant/?id="id"&name="name""
- Realizar Reserva (Form para realizar la reserva en el Restaurant previamente seleccionado): "/createreservation/?id="id"&name="name">
- Ver mis reservas (Vemos las reservas a nuestro nombre): "/myreservations/
- Modificar reservas (Modificamos la reserva seleccionada): "/updatereservation/?id="id""
- Log in (Permite iniciar sesion): "/login/"
- Registrarse (Permite crarnos un Usuario): "/register/"



