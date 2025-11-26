#codigo con empleados de ejemplo para comenzar la BD
def clear_tables(daos):
    print("--- Limpieza de tablas omitida) ---")

def populate_employees(employee_dao):
    from receptionist import Receptionist
    from bellboy import Bellboy
    print("\n--- Creando Empleados ---")
    receptionist = Receptionist(0, "Brigitte", "", "Herrera", "Rodriguez", "4421111111", "brigitte@mail.com", "Activo", "HERB001122QRO", "brigitte123")
    bellboy = Bellboy(0, "Carlos", "", "Gomez", "Solis", "4422222222", "carlos@mail.com", "Activo", "GOSC001122QRO", "carlos123")
    
    if employee_dao.create(receptionist):
        print(f"-> Empleado {receptionist.getFirstName()} creado con ID: {receptionist.getId()}")
    if employee_dao.create(bellboy):
        print(f"-> Empleado {bellboy.getFirstName()} creado con ID: {bellboy.getId()}")

def populate_customers(customer_dao):
    from customer import Customer
    print("\n--- Creando Clientes ---")
    customer1 = Customer(0, "Andrea", "Sarahi", "Lopez", "Guerrero", "4420000000", "andrea@mail.com", "Querétaro", "LOGA001122QRO", "andrea123")
    customer2 = Customer(0, "Juan", "", "Perez", "Vera", "4423333333", "juan@mail.com", "Querétaro", "PEVJ001122QRO", "juan123")
    
    if customer_dao.create(customer1):
        print(f"-> Cliente '{customer1.getName()}' creado con ID: {customer1.getId()}")
    if customer_dao.create(customer2):
        print(f"-> Cliente '{customer2.getName()}' creado con ID: {customer2.getId()}")

def populate_services(service_dao):
    from service import Service
    print("\n--- Creando Servicios ---")
    services_to_create = [
        Service(0, "Room Service 24H", 15.00, "Entrega de alimentos y bebidas a la habitacion a cualquier hora."),
        Service(0, "Lavanderia Express", 30.00, "Lavado, secado y planchado con entrega en 4 horas."),
        Service(0, "Acceso a Spa", 50.00, "Acceso a sauna, baño turco y piscina climatizada por dia."),
        Service(0, "Masaje Terapeutico", 85.00, "Sesion privada de masaje de cuerpo completo (60 minutos)."),
        Service(0, "Cama Adicional", 25.00, "Instalacion de una cama supletoria en la habitacion."),
        Service(0, "Parqueo con Valet", 10.00, "Servicio de aparcacoches y recogida del vehiculo.")
    ]
    for svc in services_to_create:
        if service_dao.create(svc):
            print(f"-> Servicio '{svc.getType()}' creado con ID: {svc.getId()}")

def populate_rooms(room_dao):
    """Puebla la tabla de habitaciones."""
    from room import Room
    print("\n--- Creando Habitaciones ---")
    rooms_to_create = [
        Room(0, "101", "Sencilla", "Available", 120.00, "Una cama Queen size, ideal para un viajero."),
        Room(0, "205", "Doble", "Available", 180.00, "Dos camas Queen size, para hasta 4 huespedes."),
        Room(0, "310", "King Size", "Not available", 220.00, "Una cama King size, con balcon privado."),
        Room(0, "401", "Suite Ejecutiva", "Available", 350.00, "Habitacion con sala de estar, minibar y escritorio de trabajo."),
        Room(0, "503", "Suite Presidencial", "Maintenance", 600.00, "La suite mas lujosa, con jacuzzi y comedor privado."),
        Room(0, "108", "Accesible", "Available", 150.00, "Habitacion adaptada para personas con movilidad reducida.")
    ]
    count = 0
    for room in rooms_to_create:
        if room_dao.create(room):
            count += 1
            print(f"-> Habitacion '{room.getType()}' creada con ID: {room.getId()}")
    print(f"-> {count} habitaciones creadas exitosamente.")

def populate_initial_data():
    """
    Usa los DAOs para insertar datos iniciales en la base de datos.
    Ejecuta este script una vez para llenar tus tablas.
    """
    print("Iniciando el poblado de la base de datos...")
    try:
        # Importaciones tardías para asegurar que la conexión a la BD se establezca primero
        from dao.employee_dao import EmployeeDAO
        from dao.ServiceDAO import ServiceDAO
        from dao.customer_dao import CustomerDAO
        from dao.room_dao import RoomDAO

        daos = {
            "employee": EmployeeDAO(),
            "service": ServiceDAO(),
            "customer": CustomerDAO(),
            "room": RoomDAO()
        }

        populate_employees(daos["employee"])
        populate_customers(daos["customer"])
        populate_services(daos["service"])
        populate_rooms(daos["room"])

        print("\n¡Poblado de la base de datos completado exitosamente!")

    except Exception as e:
        print(f"\nCRITICAL ERROR durante el poblado de la base de datos: {e}")
        print("Por favor, verifica la conexión a la BD, las variables de entorno y que las tablas existan.")

if __name__ == '__main__':
    populate_initial_data()