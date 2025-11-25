import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date

# ----------------- Clases de Lógica de Negocio (Implementación Dummy) -----------------
# Estas clases se necesitan para que el código sea completamente ejecutable y para simular la interacción.

class Customer:
    def __init__(self, id, first_name, middle_name, last_name, second_last_name, phone, email, address, rfc):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
    def getFirstName(self): return self._first_name
    def getName(self): return self._first_name # Para Customer usamos el nombre simple
    
class Room:
    def __init__(self, id, type, status, cost, description):
        self._id = id
        self._type = type
        self._status = status
        self._cost = cost
    def getId(self): return self._id
    def getType(self): return self._type
    def getCost(self): return self._cost
    def getStatus(self): return self._status
    
class Payment:
    def __init__(self, id, amount, method):
        self._id = id
        self._amount = amount
    
class Reservation:
    def __init__(self, id, check_in, check_out, customer, room, payment):
        self._id = id
        self._check_in = check_in
        self._check_out = check_out
        self._customer = customer
        self._room = room
    def getId(self): return self._id
    def getCheckIn(self): return self._check_in
    def getCheckOut(self): return self._check_out
    def getCustomer(self): return self._customer
    def getRoom(self): return self._room

class Service:
    def __init__(self, id, type, cost, description):
        self._id = id
        self._type = type
        self._cost = cost
        self._description = description
    def getType(self): return self._type
    def getDescription(self): return self._description
    def getCost(self): return self._cost

class Employee:
    def __init__(self, id, first_name, middle_name, last_name, second_last_name, phone, email, status, rfc):
        # Convertir ID a string para buscar en el diccionario de datos
        self._id = str(id) 
        self._first_name = first_name
    def getFirstName(self): return self._first_name
    def getId(self): return self._id

class Receptionist(Employee):
    def registerService(self, service): pass # Método simulado

class Bellboy(Employee):
    pass # Clase simulada

# ----------------- Funciones de Inicialización de Datos -----------------

def init_data():
    """Inicializa y retorna los objetos base y una lista de empleados/clientes para la simulación."""
    # Clientes de Ejemplo (Login: andrea@mail.com)
    customer1 = Customer(1, "Andrea", "Sarahi", "Lopez", "Guerrero", "4420000000", "andrea@mail.com", "Querétaro", "LOGA001122QRO")
    
    # Empleados de Ejemplo (Login: ID: 1, Nombre: Brigitte)
    receptionist = Receptionist(1, "Brigitte", "", "Herrera", "Rodriguez", "4421111111", "brigitte@mail.com", "Active", "HERB001122QRO")
    bellboy = Bellboy(2, "Esmeralda", "", "Vazquez", "Garcia", "4422222222", "esme@mail.com", "Active", "VAGE001122QRO")
    
    # Habitación, Pago y Reserva
    room1 = Room(101, "Suite", "Available", 1500.0, "Sea view")
    payment1 = Payment(1, 1500.0, "Credit Card")
    reservation1 = Reservation(1, date(2025, 10, 10), date(2025, 10, 15), customer1, room1, payment1)
    
    # Servicio de ejemplo y registro
    service1 = Service(1, "Spa", 300, "Full body massage")
    receptionist.registerService(service1)

    return {
        # Base de datos simple de clientes (Correo: objeto)
        'customers': {'andrea@mail.com': customer1}, 
        # Base de datos simple de empleados (ID como string: objeto)
        'employees': {'1': receptionist, '2': bellboy}, 
        'rooms': {101: room1},
        'reservations': {1: reservation1},
        'services': {1: service1}
    }

# ----------------- Clase Controladora de la Aplicación -----------------

class HotelGUI:
    """Clase principal que controla la navegación entre pantallas (frames)."""
    def __init__(self, master):
        self.master = master
        master.title("🏨 Sistema de Gestión Hotelera")
        # Establecer un tamaño fijo para la ventana
        master.geometry("650x500") 
        master.resizable(False, False) # Deshabilitar redimensionamiento para consistencia
        
        # Configuración de estilos
        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'), foreground='#004d40')
        self.style.configure('TFrame', background='#e0f2f1')
        self.style.configure('TButton', font=('Arial', 11), padding=10, background='#00796b', foreground='white')
        self.style.configure('TLabel', background='#e0f2f1', font=('Arial', 10))
        # Estilo para el botón de acceso principal
        self.style.configure('Access.TButton', font=('Arial', 13, 'bold'), padding=20, background='#009688', foreground='white')

        # Contenedor principal donde se apilan las pantallas
        self.container = ttk.Frame(master)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cargar los datos iniciales
        self.data = init_data()

        # Almacena las instancias de las pantallas
        self.frames = {}

        # Inicializa las cuatro pantallas
        for F in (WelcomeScreen, LoginFormScreen, LoginSuccessScreen, MainMenuScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Las apila en la misma celda (row=0, column=0)
            frame.grid(row=0, column=0, sticky="nsew") 

        self.show_frame("WelcomeScreen")

    def show_frame(self, page_name, user_type=None, user_obj=None, login_type=None):
        """
        Muestra la ventana (frame) solicitada.
        - user_type/user_obj: Datos para LoginSuccessScreen o MainMenuScreen.
        - login_type: Tipo de formulario a cargar en LoginFormScreen ("Employee" o "Guest").
        """
        frame = self.frames[page_name]
        
        # Si la pantalla necesita datos de usuario (éxito de login o menú)
        if page_name == "LoginSuccessScreen" or page_name == "MainMenuScreen":
            frame.set_user(user_type, user_obj)
        
        # Si la pantalla es el formulario de login, configuramos el tipo (Employee/Guest)
        elif page_name == "LoginFormScreen" and login_type:
            frame.set_login_type(login_type)
            
        frame.tkraise()

# ----------------- Pantalla de Bienvenida (Opciones Iniciales) -----------------

class WelcomeScreen(ttk.Frame):
    """Pantalla inicial para elegir entre Huésped o Empleado."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Título principal
        ttk.Label(self, text="BIENVENIDO, SELECCIONE SU TIPO DE ACCESO", style='Header.TLabel').pack(pady=30)
        
        # Frame para las dos opciones de acceso (centrado)
        access_options_frame = ttk.Frame(self)
        access_options_frame.pack(pady=40, padx=20)
        
        # Botón para Empleado
        ttk.Button(access_options_frame, text="ACCESO EMPLEADO", 
                   command=lambda: self.controller.show_frame("LoginFormScreen", login_type="Employee"),
                   style='Access.TButton', width=30).grid(row=0, column=0, padx=20, pady=10)

        # Botón para Huésped
        ttk.Button(access_options_frame, text="ACCESO HUÉSPED", 
                   command=lambda: self.controller.show_frame("LoginFormScreen", login_type="Guest"),
                   style='Access.TButton', width=30).grid(row=0, column=1, padx=20, pady=10)
        
        # Botón de Registro (Abajo)
        ttk.Button(self, text="REGISTRO (Aún no implementado)", command=self.register_user).pack(pady=30)

    def register_user(self):
        """Función placeholder para el registro."""
        messagebox.showinfo("Registro", "Esta funcionalidad de registro está pendiente de implementar.")

# ----------------- Nueva Pantalla de Formulario de Login -----------------

class LoginFormScreen(ttk.Frame):
    """Pantalla dedicada para ingresar credenciales de Empleado o Huésped."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.login_type = "" # Almacena "Employee" o "Guest"

        ttk.Label(self, text="INGRESO DE CREDENCIALES", style='Header.TLabel').pack(pady=20)

        # Contenedor central para el formulario
        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(pady=20, ipadx=40, ipady=10)
        
        # Etiqueta de título dinámico
        self.title_label = ttk.Label(self.form_frame, text="", font=('Arial', 14, 'bold'))
        self.title_label.pack(pady=10)

        # Campo 1
        self.label1 = ttk.Label(self.form_frame, text="")
        self.label1.pack(pady=5)
        self.entry1 = ttk.Entry(self.form_frame, width=30)
        self.entry1.pack(pady=5)

        # Campo 2
        self.label2 = ttk.Label(self.form_frame, text="")
        self.label2.pack(pady=5)
        self.entry2 = ttk.Entry(self.form_frame, width=30)
        self.entry2.pack(pady=5)
        
        # Botón de Login
        self.login_button = ttk.Button(self.form_frame, text="INGRESAR", command=self.attempt_login, style='Access.TButton', width=20)
        self.login_button.pack(pady=20)
        
        # Botón de Regreso
        ttk.Button(self, text="<- Volver a Elegir Acceso", command=self.go_back).pack(pady=10)
        
    def clear_form(self):
        """Limpia las entradas."""
        self.entry1.delete(0, 'end')
        self.entry2.delete(0, 'end')

    def set_login_type(self, login_type):
        """Configura el formulario para Huésped o Empleado."""
        self.login_type = login_type
        self.clear_form() # Limpiar entradas al cambiar de tipo
        
        if login_type == "Employee":
            self.title_label.config(text="ACCESO PARA EMPLEADOS")
            self.label1.config(text="ID de Empleado (Contraseña):")
            self.entry1.config(show="*")
            self.label2.config(text="Nombre (Usuario):")
            self.entry2.config(show="") # Nombre es visible
            
            # Poner datos de demo automáticamente (opcional para facilitar la prueba)
            self.entry1.insert(0, "1")
            self.entry2.insert(0, "Brigitte")

        elif login_type == "Guest":
            self.title_label.config(text="ACCESO PARA HUÉSPEDES")
            self.label1.config(text="Correo (Usuario):")
            self.entry1.config(show="") # Correo es visible
            self.label2.config(text="Contraseña (Cualquiera):")
            self.entry2.config(show="*")

            # Poner datos de demo automáticamente (opcional para facilitar la prueba)
            self.entry1.insert(0, "andrea@mail.com")
            self.entry2.insert(0, "password123")


    def attempt_login(self):
        """Intenta el login basado en el tipo de usuario configurado."""
        entry1_value = self.entry1.get().strip()
        entry2_value = self.entry2.get().strip()

        if not entry1_value or not entry2_value:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese ambos campos.")
            return

        if self.login_type == "Employee":
            self.login_employee(entry1_value, entry2_value)
        elif self.login_type == "Guest":
            self.login_guest(entry1_value, entry2_value)

    def login_employee(self, emp_id, emp_name):
        """Valida el acceso del empleado."""
        employees = self.controller.data['employees']
        employee_obj = employees.get(emp_id)

        # Validar tanto el ID como el nombre del empleado
        if employee_obj and employee_obj.getFirstName().lower() == emp_name.lower():
            self.controller.show_frame("LoginSuccessScreen", user_type="Empleado", user_obj=employee_obj)
        else:
            messagebox.showerror("Error de Login", "ID o Nombre de empleado incorrectos. Use ID: '1', Nombre: 'Brigitte' para la demo.")

    def login_guest(self, email, password):
        """Valida el acceso del huésped."""
        customers = self.controller.data['customers']
        customer_obj = customers.get(email)

        # Validación simple (solo revisa si el correo existe)
        if customer_obj:
            # Nota: No se valida la contraseña para la demo, solo la existencia del correo.
            self.controller.show_frame("LoginSuccessScreen", user_type="Huésped", user_obj=customer_obj)
        else:
            messagebox.showerror("Error de Login", "Correo incorrecto. Use 'andrea@mail.com' para la demo.")

    def go_back(self):
        """Vuelve a la pantalla de bienvenida."""
        self.controller.show_frame("WelcomeScreen")

# ----------------- Pantalla de Éxito de Login (Intermedia) -----------------

class LoginSuccessScreen(ttk.Frame):
    """Pantalla de confirmación después de un login exitoso, antes de entrar al menú."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_type = None
        self.user_obj = None

        self.welcome_text = tk.StringVar(self, value="")
        
        # Título
        ttk.Label(self, text="¡ACCESO CONCEDIDO!", style='Header.TLabel', foreground='#009688').pack(pady=30)
        
        # Mensaje de bienvenida dinámico
        ttk.Label(self, textvariable=self.welcome_text, font=('Arial', 14)).pack(pady=20)

        # Botón para entrar al sistema
        ttk.Button(self, text="ENTRAR AL SISTEMA", command=self.go_to_main_menu, 
                   style='Access.TButton', width=40).pack(pady=40, ipadx=20, ipady=15)
        
        # Botón de Cerrar Sesión (Opción)
        ttk.Button(self, text="Cerrar Sesión", command=self.logout, style='TButton').pack(pady=10)

    def set_user(self, user_type, user_obj):
        """Almacena el usuario y actualiza el mensaje de bienvenida."""
        self.user_type = user_type
        self.user_obj = user_obj
        
        # Obtener el nombre
        if self.user_obj:
            # Usamos getFirstName para Employee/Receptionist/Bellboy y getName para Customer
            name = self.user_obj.getFirstName() if hasattr(self.user_obj, 'getFirstName') else self.user_obj.getName()
            self.welcome_text.set(f"Bienvenido/a, {name} ({user_type}).\nPresione el botón para acceder al menú principal.")
        else:
             self.welcome_text.set("Error al cargar datos de usuario. Intente iniciar sesión de nuevo.")


    def go_to_main_menu(self):
        """Navega al menú principal con la información del usuario."""
        if self.user_obj:
            # Navega al menú principal, pasando el usuario y tipo
            self.controller.show_frame("MainMenuScreen", user_type=self.user_type, user_obj=self.user_obj)
        else:
            messagebox.showerror("Error", "No hay datos de usuario para ingresar.")
            self.controller.show_frame("WelcomeScreen")

    def logout(self):
        """Cierra sesión y regresa a la pantalla de bienvenida."""
        self.user_type = None
        self.user_obj = None
        messagebox.showinfo("Cerrar Sesión", "Sesión finalizada. Volviendo al inicio.")
        self.controller.show_frame("WelcomeScreen")

# ----------------- Pantalla del Menú Principal -----------------

class MainMenuScreen(ttk.Frame):
    """Pantalla con las opciones principales de gestión."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_type = None
        self.user_obj = None

        self.welcome_label = ttk.Label(self, text="", style='Header.TLabel', foreground='#004d40')
        self.welcome_label.pack(pady=15)
        
        # Frame para organizar los botones en una cuadrícula
        menu_frame = ttk.Frame(self)
        menu_frame.pack(pady=20)

        # Botones del menú
        options = [
            ("Crear Reserva de Habitación", self.create_room_reservation),
            ("Crear Reserva de Servicio", self.create_service_reservation),
            ("Ver Info de las Habitaciones", self.view_room_info),
            ("Ver Reserva de Habitación", self.view_room_reservation),
            ("Ver Reserva de Servicio", self.view_service_reservation)
        ]
        
        for i, (text, command) in enumerate(options):
            row = i // 2
            col = i % 2
            ttk.Button(menu_frame, text=text, command=command, width=30).grid(row=row, column=col, padx=15, pady=15, ipadx=10, ipady=10)

        # Botón de Cerrar Sesión
        ttk.Button(self, text="Cerrar Sesión", command=self.logout, style='TButton').pack(pady=30)


    def set_user(self, user_type, user_obj):
        """Actualiza la etiqueta de bienvenida con el nombre del usuario."""
        self.user_type = user_type
        self.user_obj = user_obj
        
        # Usamos getFirstName para Employee/Receptionist/Bellboy y getName para Customer
        name = self.user_obj.getFirstName() if hasattr(self.user_obj, 'getFirstName') else self.user_obj.getName()
        self.welcome_label.config(text=f"Menú Principal ({user_type}) - ¡Hola, {name}!")

    # ------------------- Funcionalidades del Menú -------------------

    def create_room_reservation(self):
        messagebox.showinfo("Funcionalidad", "Función: Crear Reserva de Habitación (Pendiente).")

    def create_service_reservation(self):
        # Muestra la información del servicio de ejemplo
        service_obj = self.controller.data['services'][1]
        info = f"Servicio: {service_obj.getType()}\nDescripción: {service_obj.getDescription()}\nCosto: ${service_obj.getCost()}"
        messagebox.showinfo("Funcionalidad", f"Función: Crear Reserva de Servicio (Pendiente).\n\nServicio de ejemplo:\n{info}")

    def view_room_info(self):
        # Muestra la información de la habitación de ejemplo
        room = self.controller.data['rooms'][101]
        info = (
            f"--- Habitación {room.getId()} ---\n"
            f"Tipo: {room.getType()}\n"
            f"Precio: ${room.getCost():.2f}\n"
            f"Estado: {room.getStatus()}"
        )
        messagebox.showinfo("Información", info)

    def view_room_reservation(self):
        # Muestra la información de la reserva de ejemplo
        res = self.controller.data['reservations'][1]
        info = (
            f"--- Reserva #{res.getId()} ---\n"
            f"Cliente: {res.getCustomer().getName()}\n"
            f"Habitación: {res.getRoom().getId()} ({res.getRoom().getType()})\n"
            f"Check-In: {res.getCheckIn()}\n"
            f"Check-Out: {res.getCheckOut()}"
        )
        messagebox.showinfo("Información", info)

    def view_service_reservation(self):
        messagebox.showinfo("Funcionalidad", "Función: Ver Reserva de Servicio (Pendiente).")
    
    def logout(self):
        """Cierra sesión y regresa a la pantalla de bienvenida."""
        # Limpia los datos de usuario al cerrar sesión
        self.user_type = None
        self.user_obj = None
        messagebox.showinfo("Cerrar Sesión", "Sesión finalizada. Volviendo al inicio.")
        self.controller.show_frame("WelcomeScreen")

# ----------------- Ejecución de la Aplicación -----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelGUI(root)
    root.mainloop()