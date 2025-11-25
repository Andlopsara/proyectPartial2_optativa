import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
import re 
import uuid 

# Importar clases de POO
from customer import Customer
from service import Service 
from reservationService import ServiceReservation 
from reservation import Reservation 
from room import Room
from employee import Employee
from receptionist import Receptionist
from bellboy import Bellboy
from payment import Payment

# ----------------- Definición Global de Colores -----------------
PASTEL_BG = '#E1F5FE'      # Fondo muy claro (Light Blue 50)
PASTEL_ACCENT = '#4FC3F7'  # Azul medio para botones (Light Blue 400)
PASTEL_HEADER = '#0288D1'  # Azul oscuro para títulos (Light Blue 700)
TEXT_COLOR = 'black'       # Color de texto negro para máxima visibilidad

# ----------------- Funciones de Inicialización de Datos -----------------

def init_data():
    """Inicializa datos de demo usando las clases POO."""
    
    # Clientes de Demo (usando la clase Customer importada)
    customer1 = Customer(1, "Andrea", "Sarahi", "Lopez", "Guerrero", "4420000000", "andrea@mail.com", "Querétaro", "LOGA001122QRO", password="andrea123")
    customer2 = Customer(2, "Juan", "", "Perez", "Vera", "4423333333", "juan@mail.com", "Querétaro", "PEVJ001122QRO", password="juan123")
    
    # Empleados de Demo (usando la clase Receptionist importada)
    receptionist = Receptionist(1, "Brigitte", "", "Herrera", "Rodriguez", "4421111111", "brigitte@mail.com", "Active", "HERB001122QRO", password="brigitte123")
    
    # Habitaciones de Demo (usando la clase Room importada)
    # Crear 100 habitaciones (IDs 101-200) con diferentes tipos y precios
    rooms = {}
    room_types = ["Suite", "Doble", "Individual"]
    room_costs = {"Suite": 1500.0, "Doble": 900.0, "Individual": 600.0}
    
    import random
    random.seed(42)  # Para reproducibilidad
    
    for i in range(100):
        room_id = 101 + i
        room_type = room_types[i % 3]  # Distribuir tipos
        cost = room_costs[room_type]
        # 20% de probabilidad de que esté ocupada
        status = "Not available" if random.random() < 0.2 else "Available"
        description = f"{room_type} room with capacity for {2 if room_type == 'Individual' else 4} persons"
        rooms[room_id] = Room(room_id, room_type, status, cost, description)
    
    # Servicios Disponibles (usando la clase Service importada)
    service1 = Service(1, "Desayuno a la Habitación", 150.0, "Desayuno continental entregado en la habitación.")
    service2 = Service(2, "Lavandería Express", 200.0, "Lavado y planchado en menos de 3 horas.")
    service3 = Service(3, "Masaje Relajante", 500.0, "Sesión de masaje de 60 minutos.")
    
    # Reserva de Habitación Inicial (para demo)
    # Se simula que room 103 está ocupada por customer1
    reservation1 = Reservation(1, "2025-10-10", "2025-10-15", customer1, rooms[103], None)
    rooms[103].setStatus("Not available") 
    customer1.makeReservation(reservation1)
    
    # NUEVA RESERVA DE SERVICIO INICIAL (para demo)
    service_reservation1 = ServiceReservation(101, "2025-10-11 08:00", customer1, service1)
    customer1.makeServiceReservation(service_reservation1)
    
    # NUEVA RESERVA DE SERVICIO PARA CLIENTE 2 (para demo)
    service_reservation2 = ServiceReservation(102, "2025-10-12 12:30", customer2, service3)
    customer2.makeServiceReservation(service_reservation2)
    
    return {
        'customers': {c.getEmail(): c for c in [customer1, customer2]}, 
        'employees': {'1': receptionist}, 
        'rooms': rooms,
        'reservations': {1: reservation1}, # Solo reservas de habitación
        'service_reservations': {101: service_reservation1, 102: service_reservation2}, # NUEVO: Reservas de servicio
        'services': {s.getId(): s for s in [service1, service2, service3]} # NUEVO: Servicios disponibles
    }

# ----------------- Clase Controladora de la Aplicación -----------------

class HotelGUI:
    def __init__(self, master):
        self.master = master
        master.title("🏨 Sistema de Gestión Hotelera")
        master.geometry("550x450") 
        master.resizable(False, False) 
        
        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'), foreground=TEXT_COLOR, background=PASTEL_BG)
        self.style.configure('TFrame', background=PASTEL_BG)
        self.style.configure('TButton', font=('Arial', 10, 'bold'), padding=10, background=PASTEL_ACCENT, foreground=TEXT_COLOR, borderwidth=0)
        self.style.map('TButton', background=[('active', PASTEL_HEADER)]) 
        self.style.configure('TLabel', background=PASTEL_BG, font=('Arial', 10), foreground=TEXT_COLOR)
        self.style.configure('Access.TButton', font=('Arial', 12, 'bold'), padding=15, background=PASTEL_ACCENT, foreground=TEXT_COLOR, borderwidth=0)
        self.style.map('Access.TButton', background=[('active', PASTEL_HEADER)])

        self.container = ttk.Frame(master)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.data = init_data()
        
        # Inicialización de IDs (Se debe hacer después de init_data)
        self.next_reservation_id = max(self.data['reservations'].keys()) + 1 if self.data['reservations'] else 1
        self.next_service_reservation_id = max(self.data['service_reservations'].keys()) + 1 if self.data['service_reservations'] else 1
        self.next_payment_id = 1  # Contador para pagos
        
        # Diccionario para almacenar pagos
        self.data['payments'] = {}
        
        self.frames = {}

        # Definición de Frames
        for F in (WelcomeScreen, LoginFormScreen, LoginSuccessScreen, MainMenuScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew") 

        self.show_frame("WelcomeScreen")

    def show_frame(self, page_name, user_type=None, user_obj=None, login_type=None):
        frame = self.frames[page_name]
        
        if page_name == "LoginSuccessScreen" or page_name == "MainMenuScreen":
            frame.set_user(user_type, user_obj)
        elif page_name == "LoginFormScreen" and login_type:
            frame.set_login_type(login_type)
            
        frame.tkraise()
        
    def add_new_reservation(self, new_reservation):
        """Añade una nueva reserva de HABITACIÓN."""
        res_id = self.next_reservation_id
        self.data['reservations'][res_id] = new_reservation
        self.next_reservation_id += 1
        return res_id

    def add_new_service_reservation(self, new_service_reservation):
        """Añade una nueva reserva de SERVICIO."""
        res_id = self.next_service_reservation_id
        self.data['service_reservations'][res_id] = new_service_reservation
        self.next_service_reservation_id += 1
        return res_id

    def add_new_customer(self, customer_obj):
        """Añade un nuevo cliente a la base de datos central."""
        # customer_obj.registerCustomer() # Ejecución de método POO
        self.data['customers'][customer_obj.getEmail()] = customer_obj
        print(f"GUI Controller: Cliente {customer_obj.getName()} añadido al sistema.")
        return customer_obj

    def add_new_employee(self, employee_obj):
        """Añade un nuevo empleado a la base de datos central."""
        # Guardamos usando la ID como string para mantener compatibilidad con init_data
        key = str(employee_obj.getId())
        self.data['employees'][key] = employee_obj
        print(f"GUI Controller: Empleado {employee_obj.getFirstName()} añadido al sistema (ID {key}).")
        return employee_obj

    def add_new_payment(self, payment_obj):
        """Añade un nuevo pago a la base de datos central."""
        pay_id = self.next_payment_id
        self.data['payments'][pay_id] = payment_obj
        self.next_payment_id += 1
        print(f"GUI Controller: Pago #{pay_id} procesado por ${payment_obj.getAmount():.2f}")
        return payment_obj

# ----------------- Pantalla de Creación de Reserva de Servicio (NUEVA) -----------------

class CreateServiceReservationWindow(tk.Toplevel):
    """Ventana modal para la creación de una reserva de servicio."""
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Solicitar Nuevo Servicio")
        self.geometry("450x450")
        self.resizable(False, False)
        self.configure(bg=PASTEL_BG)

        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="NUEVA RESERVA DE SERVICIO", style='Header.TLabel', foreground=PASTEL_HEADER).pack(pady=10)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=15, padx=10)
        
        # Customer Email
        ttk.Label(form_frame, text="Email del Cliente (Ej: andrea@mail.com):").grid(row=0, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Llenar con el email del usuario logueado si es cliente
        if controller.frames['MainMenuScreen'].user_type == 'Customer' and controller.frames['MainMenuScreen'].user_obj:
            self.email_entry.insert(0, controller.frames['MainMenuScreen'].user_obj.getEmail())
            self.email_entry.config(state='readonly')
        else:
            self.email_entry.insert(0, "andrea@mail.com") # Dato de demo para empleado/recepcionista

        # Service Selection
        ttk.Label(form_frame, text="Seleccionar Servicio:").grid(row=1, column=0, sticky="w", pady=5)
        
        self.services = self.controller.data['services']
        # Combobox Options: 'ID: Tipo (Costo)'
        service_options = [f"{s.getId()}: {s.getType()} (${s.getCost():.2f})" for s in self.services.values()]
        
        self.service_var = tk.StringVar(form_frame)
        self.service_combo = ttk.Combobox(form_frame, textvariable=self.service_var, values=service_options, state="readonly", width=28)
        self.service_combo.grid(row=1, column=1, padx=10, pady=5)
        self.service_combo.set(service_options[0] if service_options else "") # Seleccionar el primero por defecto

        # Date/Time
        ttk.Label(form_frame, text="Fecha/Hora Solicitada (AAAA-MM-DD HH:MM):").grid(row=2, column=0, sticky="w", pady=5)
        self.datetime_entry = ttk.Entry(form_frame, width=30)
        self.datetime_entry.grid(row=2, column=1, padx=10, pady=5)
        self.datetime_entry.insert(0, str(date.today()) + " 10:00") # Fecha y hora de hoy por defecto
        
        # Botón de creación
        ttk.Button(main_frame, text="SOLICITAR SERVICIO", command=self.process_service_reservation, 
                   style='Access.TButton', width=25).pack(pady=30)

    def validate_datetime(self, dt_str):
        """Valida un formato simple AAAA-MM-DD HH:MM."""
        return re.match(r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}$', dt_str)

    def process_service_reservation(self):
        """Recoge datos, valida y ejecuta la lógica de creación de reserva de servicio POO."""
        email = self.email_entry.get().strip()
        service_info = self.service_var.get().strip()
        date_time_str = self.datetime_entry.get().strip()

        # Validación básica de campos
        if not all([email, service_info, date_time_str]):
            messagebox.showwarning("Datos Incompletos", "Todos los campos son obligatorios.")
            return
        
        if not self.validate_datetime(date_time_str):
            messagebox.showerror("Error de Formato", "El formato de Fecha/Hora debe ser AAAA-MM-DD HH:MM.")
            return

        # 1. Buscar Cliente
        customer_obj = self.controller.data['customers'].get(email)
        if not customer_obj:
            messagebox.showerror("Error de Cliente", f"Cliente con email '{email}' no encontrado.")
            return

        # 2. Obtener el ID del Servicio
        try:
            service_id = int(service_info.split(':')[0])
            service_obj = self.services.get(service_id)
        except:
            messagebox.showerror("Error de Servicio", "Selección de servicio no válida.")
            return
        
        if not service_obj:
            messagebox.showerror("Error de Servicio", "El servicio seleccionado no existe.")
            return

        # 3. Crear Objeto ServiceReservation
        new_res_id = self.controller.next_service_reservation_id
        
        reservation = ServiceReservation(
            new_res_id,
            date_time_str,
            customer_obj,
            service_obj
        )

        # 4. Ejecutar la lógica POO y actualizar la base de datos
        if reservation.createReservation():
            self.controller.add_new_service_reservation(reservation) # Actualiza el estado global
            messagebox.showinfo("Reserva de Servicio Exitosa", 
                                f"Servicio '{service_obj.getType()}' solicitado con éxito para {customer_obj.getName()}. Reserva #{new_res_id}.")
            self.destroy() # Cierra la ventana modal
        else:
            messagebox.showerror("Reserva Fallida", "No se pudo crear la reserva de servicio.")


# Declaraciones anticipadas de clases (forward references)
class RegisterCustomerWindow(tk.Toplevel):
    pass

class RegisterEmployeeWindow(tk.Toplevel):
    pass

# Reemplazaremos estas con las implementaciones reales después de las otras clases

# ----------------- Pantallas de la Aplicación -----------------

# (WelcomeScreen y LoginFormScreen sin cambios)
class WelcomeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        ttk.Label(self, text="BIENVENIDO A HOTEL LE VILLA", style='Header.TLabel', foreground=PASTEL_HEADER).pack(pady=40)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="ACCESO HUÉSPED", style='Access.TButton', width=20, 
                   command=lambda: controller.show_frame("LoginFormScreen", login_type="Customer")).grid(row=0, column=0, padx=10)
                   
        ttk.Button(btn_frame, text="ACCESO EMPLEADO", style='Access.TButton', width=20, 
                   command=lambda: controller.show_frame("LoginFormScreen", login_type="Employee")).grid(row=0, column=1, padx=10)
        
        # Botones de registro rápidos en la pantalla inicial
        ttk.Button(btn_frame, text="REGISTRAR HUÉSPED", width=20, 
               command=lambda: RegisterCustomerWindow(controller.master, controller)).grid(row=1, column=0, pady=8)
        ttk.Button(btn_frame, text="REGISTRAR EMPLEADO", width=20, 
               command=lambda: RegisterEmployeeWindow(controller.master, controller)).grid(row=1, column=1, pady=8)

class LoginFormScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.login_type = ""
        
        self.title_label = ttk.Label(self, text="INICIO DE SESIÓN", style='Header.TLabel', foreground=PASTEL_HEADER)
        self.title_label.pack(pady=40)
        
        ttk.Label(self, text="Email:").pack(pady=5)
        self.email_entry = ttk.Entry(self, width=30)
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, "andrea@mail.com") # Demo customer email

        ttk.Label(self, text="Contraseña (Ignorada en Demo):").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=5)
        
        ttk.Button(self, text="INGRESAR", command=self.login, style='Access.TButton').pack(pady=20)
        ttk.Button(self, text="Volver", command=lambda: controller.show_frame("WelcomeScreen")).pack(pady=10)
        
    def set_login_type(self, login_type):
        self.login_type = login_type
        if login_type == "Customer":
            self.title_label.config(text="ACCESO HUÉSPED")
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, "andrea@mail.com") # Demo customer
        else: # Employee
            self.title_label.config(text="ACCESO EMPLEADO")
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, "brigitte@mail.com") # Demo employee

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if self.login_type == "Customer":
            user_obj = self.controller.data['customers'].get(email)
            if user_obj and user_obj.getPassword() == password:
                messagebox.showinfo("Éxito", f"Bienvenido, Huésped {user_obj.getName()}")
                self.controller.show_frame("MainMenuScreen", user_type="Customer", user_obj=user_obj)
            else:
                messagebox.showerror("Error", "Email o contraseña de Huésped incorrectos. Intente con 'andrea@mail.com' / 'andrea123' o 'juan@mail.com' / 'juan123'")
        else: # Employee
            # Buscamos por email en empleados y validamos contraseña
            user_obj = next((emp for emp in self.controller.data['employees'].values() if getattr(emp, 'getEmail', lambda: None)() == email), None)

            if user_obj and user_obj.getPassword() == password:
                messagebox.showinfo("Éxito", f"Bienvenido, Empleado {user_obj.getFirstName()}")
                self.controller.show_frame("MainMenuScreen", user_type="Employee", user_obj=user_obj)
            else:
                messagebox.showerror("Error", "Email o contraseña de Empleado incorrectos. Intente con 'brigitte@mail.com' / 'brigitte123'")


class LoginSuccessScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_type = None
        self.user_obj = None
        
        self.welcome_label = ttk.Label(self, text="", style='Header.TLabel', foreground=PASTEL_HEADER)
        self.welcome_label.pack(pady=40)
        
        ttk.Button(self, text="Ir al Menú Principal", command=lambda: controller.show_frame("MainMenuScreen"), style='Access.TButton').pack(pady=20)
        ttk.Button(self, text="Cerrar Sesión", command=lambda: controller.show_frame("WelcomeScreen")).pack(pady=10)

    def set_user(self, user_type, user_obj):
        self.user_type = user_type
        self.user_obj = user_obj
        if user_obj:
            self.welcome_label.config(text=f"¡Bienvenido/a, {user_obj.getFirstName()}!")
        else:
            self.welcome_label.config(text="¡Bienvenido/a!")


class MainMenuScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_type = None
        self.user_obj = None
        
        # Título y Frame de bienvenida
        self.header_label = ttk.Label(self, text="MENÚ PRINCIPAL", style='Header.TLabel', foreground=PASTEL_HEADER)
        self.header_label.pack(pady=10)
        self.role_label = ttk.Label(self, text="", font=('Arial', 12, 'italic'))
        self.role_label.pack(pady=5)

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, padx=20, pady=10)
        
        self.menu_buttons = []
        self._setup_layout()

    def _setup_layout(self):
        """Define la cuadrícula de botones genéricos."""
        
        # Limpiar botones anteriores
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        self.menu_buttons.clear()

        # Botones Genéricos (Visibles para todos)
        ttk.Button(self.main_frame, text="Ver Info. Hab. (101)", command=self.view_room_info).grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        # Botón de prueba para abrir la ventana de pago de la última reserva (útil para debug/QA)
        ttk.Button(self.main_frame, text="Abrir Pago (última)", command=self.open_last_payment).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Botones específicos que se modificarán en set_user
        self.btn_reserva_hab = ttk.Button(self.main_frame, text="Crear Reserva Hab.", command=self.open_create_reservation).grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        
        # NUEVO BOTÓN: Reserva de Servicio
        self.btn_reserva_servicio = ttk.Button(self.main_frame, text="Solicitar Servicio", command=self.open_create_service_reservation).grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # NUEVO BOTÓN: Ver Reservas de Habitación
        self.btn_view_room_res = ttk.Button(self.main_frame, text="Ver Reservas Hab.", command=self.view_room_reservation).grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        
        # NUEVO BOTÓN: Ver Reservas de Servicio
        self.btn_view_service_res = ttk.Button(self.main_frame, text="Ver Reservas Servicio", command=self.view_service_reservation).grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        # Botón de Salir/Logout
        ttk.Button(self.main_frame, text="Cerrar Sesión", command=lambda: self.controller.show_frame("WelcomeScreen")).grid(row=3, column=0, columnspan=2, padx=5, pady=20, sticky='ew')
        
    def set_user(self, user_type, user_obj):
        """Ajusta el menú en función del tipo de usuario."""
        self.user_type = user_type
        self.user_obj = user_obj
        
        self._setup_layout() # Redibuja los botones
        
        if user_type == "Customer":
            self.role_label.config(text=f"Huésed: {user_obj.getName()}")
            # Huéspedes no pueden registrar nuevos clientes (aunque el botón no está)
            # Todos los botones son visibles.
            
        elif user_type == "Employee":
            self.role_label.config(text=f"Empleado: {user_obj.getFirstName()}")
            # Empleados ven todos los botones.

        # Actualizar texto del botón de reserva de habitación
        # (No es necesario actualizar texto, solo la lógica de las funciones, que ya lo hace)


    # ------------------- Funcionalidades del Menú (Acciones) -------------------

    def open_create_reservation(self):
        """Abre la ventana modal para crear una reserva de habitación."""
        if self.user_type == 'Customer':
            CreateReservationWindow(self.controller.master, self.controller)
        elif self.user_type == 'Employee':
            CreateReservationWindow(self.controller.master, self.controller)


    def open_create_service_reservation(self):
        """Abre la ventana modal para crear una reserva de servicio."""
        # Esta acción es válida tanto para huéspedes (solicitar servicio) como para empleados (registrar solicitud).
        CreateServiceReservationWindow(self.controller.master, self.controller)

    def open_last_payment(self):
        """Abre la ventana de pago para la última reserva registrada (para pruebas)."""
        if not self.controller.data.get('reservations'):
            messagebox.showinfo("Sin Reservas", "No hay reservas registradas para mostrar el pago.")
            return

        try:
            last_id = max(self.controller.data['reservations'].keys())
            reservation = self.controller.data['reservations'][last_id]
        except Exception:
            messagebox.showerror("Error", "No se pudo obtener la última reserva.")
            return

        # Calcular costo total según noches
        from datetime import datetime
        try:
            check_in = datetime.strptime(reservation.getCheckIn(), "%Y-%m-%d").date()
            check_out = datetime.strptime(reservation.getCheckOut(), "%Y-%m-%d").date()
            num_nights = (check_out - check_in).days
            if num_nights < 1:
                num_nights = 1
        except Exception:
            num_nights = 1

        room = reservation.getRoom()
        total_cost = room.getCost() * num_nights

        PaymentWindow(self.controller.master, self.controller, reservation, total_cost, reservation.getCustomer())


    def view_room_info(self):
        """Muestra información de una habitación de demo."""
        room = self.controller.data['rooms'][101]
        info = (
            f"Habitación {room.getId()} ({room.getType()})\n"
            f"Precio: ${room.getCost():.2f}\n"
            f"Estado: {room.getStatus()}"
        )
        messagebox.showinfo("Información de Habitación", info)


    def view_room_reservation(self):
        """
        Muestra reservas de habitación.
        - Empleado: Muestra TODAS las reservas.
        - Huésped: Muestra SÓLO sus reservas.
        """
        reservations = []
        if self.user_type == 'Employee':
            reservations = list(self.controller.data['reservations'].values())
            title = "Todas las Reservas de Habitación (Empleado)"
        elif self.user_type == 'Customer':
            reservations = self.user_obj.getReservations()
            title = f"Reservas de Habitación de {self.user_obj.getName()}"

        if not reservations:
            messagebox.showinfo(title, "No se encontraron reservas de habitación.")
            return

        info_list = "\n\n".join([res.showInfo() for res in reservations])
        messagebox.showinfo(title, info_list)


    def view_service_reservation(self):
        """
        Muestra reservas de servicio.
        - Empleado: Muestra TODAS las reservas.
        - Huésped: Muestra SÓLO sus reservas.
        """
        service_reservations = []
        if self.user_type == 'Employee':
            service_reservations = list(self.controller.data['service_reservations'].values())
            title = "Todas las Reservas de Servicio (Empleado)"
        elif self.user_type == 'Customer':
            service_reservations = self.user_obj.getServiceReservations()
            title = f"Reservas de Servicio de {self.user_obj.getName()}"

        if not service_reservations:
            messagebox.showinfo(title, "No se encontraron reservas de servicio.")
            return

        info_list = "\n\n".join([res.showInfo() for res in service_reservations])
        messagebox.showinfo(title, info_list)


    def register_customer(self):
        """Abre la ventana modal para registrar un nuevo cliente."""
        RegisterCustomerWindow(self.controller.master, self.controller)
        
    def register_employee(self):
        """Abre la ventana modal para registrar un nuevo empleado."""
        RegisterEmployeeWindow(self.controller.master, self.controller)
        
    def manage_rooms(self):
        messagebox.showinfo("Pendiente", "Función: Administrar Habitaciones (CRUD).")


# ----------------- Pantalla de Creación de Reserva de Habitación (Clase anterior) -----------------
class CreateReservationWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Crear Nueva Reserva de Habitación")
        self.geometry("550x600")
        self.resizable(False, False)
        self.configure(bg=PASTEL_BG)

        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="NUEVA RESERVA DE HABITACIÓN", style='Header.TLabel', foreground=PASTEL_HEADER).pack(pady=10)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg=PASTEL_BG, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        form_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        
        # Actualizar región scrollable
        form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Customer Email
        ttk.Label(form_frame, text="Email del Cliente (Ej: juan@mail.com):").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.email_entry = ttk.Entry(form_frame, width=40)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Llenar con el email del usuario logueado si es cliente
        if controller.frames['MainMenuScreen'].user_type == 'Customer' and controller.frames['MainMenuScreen'].user_obj:
            self.email_entry.insert(0, controller.frames['MainMenuScreen'].user_obj.getEmail())
            self.email_entry.config(state='readonly')
        else:
            self.email_entry.insert(0, "juan@mail.com")
        
        # Tipo de Habitación
        ttk.Label(form_frame, text="Tipo de Habitación:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.room_type_var = tk.StringVar(value="Suite")
        room_type_combo = ttk.Combobox(form_frame, textvariable=self.room_type_var, 
                                       values=["Suite", "Doble", "Individual"], state="readonly", width=37)
        room_type_combo.grid(row=1, column=1, padx=5, pady=5)
        room_type_combo.bind("<<ComboboxSelected>>", self.update_available_rooms)
        
        # Información de disponibilidad
        ttk.Label(form_frame, text="Habitaciones Disponibles:").grid(row=2, column=0, sticky="nw", pady=5, padx=5)
        
        # Frame con scroll para mostrar habitaciones disponibles
        rooms_frame = ttk.Frame(form_frame)
        rooms_frame.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        rooms_canvas = tk.Canvas(rooms_frame, bg=PASTEL_BG, highlightthickness=0, width=280, height=120)
        rooms_canvas.pack(side="left", fill="both", expand=True)
        
        rooms_scrollbar = ttk.Scrollbar(rooms_frame, orient="vertical", command=rooms_canvas.yview)
        rooms_scrollbar.pack(side="right", fill="y")
        
        rooms_canvas.configure(yscrollcommand=rooms_scrollbar.set)
        
        self.rooms_inner_frame = ttk.Frame(rooms_canvas)
        rooms_canvas.create_window((0, 0), window=self.rooms_inner_frame, anchor="nw")
        
        self.rooms_inner_frame.bind(
            "<Configure>",
            lambda e: rooms_canvas.configure(scrollregion=rooms_canvas.bbox("all"))
        )
        
        self.rooms_canvas = rooms_canvas
        self.room_selection_var = tk.StringVar()
        
        # Check-In Date
        ttk.Label(form_frame, text="Fecha de Check-In (AAAA-MM-DD):").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.check_in_entry = ttk.Entry(form_frame, width=40)
        self.check_in_entry.grid(row=3, column=1, padx=5, pady=5)
        self.check_in_entry.insert(0, str(date.today()))
        
        # Check-Out Date
        ttk.Label(form_frame, text="Fecha de Check-Out (AAAA-MM-DD):").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.check_out_entry = ttk.Entry(form_frame, width=40)
        self.check_out_entry.grid(row=4, column=1, padx=5, pady=5)
        self.check_out_entry.insert(0, "2025-12-31")
        
        # Número de Personas
        ttk.Label(form_frame, text="Número de Personas:").grid(row=5, column=0, sticky="w", pady=5, padx=5)
        self.people_spinbox = ttk.Spinbox(form_frame, from_=1, to=4, width=38)
        self.people_spinbox.grid(row=5, column=1, padx=5, pady=5)
        self.people_spinbox.set(2)
        
        # Botón de confirmación
        ttk.Button(main_frame, text="CONFIRMAR RESERVA", command=self.process_reservation, 
                   style='Access.TButton', width=30).pack(pady=20)
        
        # Mostrar habitaciones disponibles inicialmente
        self.update_available_rooms()

    def update_available_rooms(self, event=None):
        """Actualiza la lista de habitaciones disponibles según el tipo seleccionado."""
        # Limpiar el frame anterior
        for widget in self.rooms_inner_frame.winfo_children():
            widget.destroy()
        
        room_type = self.room_type_var.get()
        available_rooms = [r for r in self.controller.data['rooms'].values() 
                          if r.getType() == room_type and r.getStatus() == "Available"]
        
        if not available_rooms:
            ttk.Label(self.rooms_inner_frame, text="No hay habitaciones disponibles de este tipo.").pack(anchor="w")
            return
        
        for i, room in enumerate(sorted(available_rooms, key=lambda x: x.getId())):
            cost = room.getCost()
            label_text = f"Habitación {room.getId()} - ${cost:.2f}/noche"
            rb = ttk.Radiobutton(self.rooms_inner_frame, text=label_text, variable=self.room_selection_var, 
                                value=str(room.getId()))
            rb.pack(anchor="w")
        
        # Seleccionar la primera por defecto
        if available_rooms:
            self.room_selection_var.set(str(available_rooms[0].getId()))

    def validate_date(self, date_str):
        """Valida un formato de fecha simple AAAA-MM-DD."""
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return False
        try:
            date.fromisoformat(date_str)
            return True
        except ValueError:
            return False

    def process_reservation(self):
        """Recoge datos, valida y ejecuta la lógica de creación de reserva POO."""
        email = self.email_entry.get().strip()
        room_id_str = self.room_selection_var.get().strip()
        check_in_str = self.check_in_entry.get().strip()
        check_out_str = self.check_out_entry.get().strip()
        num_people = self.people_spinbox.get().strip()

        if not all([email, room_id_str, check_in_str, check_out_str, num_people]):
            messagebox.showwarning("Datos Incompletos", "Todos los campos son obligatorios.")
            return
        
        if not self.validate_date(check_in_str) or not self.validate_date(check_out_str):
            messagebox.showerror("Error de Formato", "El formato de fecha debe ser AAAA-MM-DD.")
            return
        
        try:
            room_id = int(room_id_str)
        except ValueError:
            messagebox.showerror("Error de ID", "El ID de la habitación debe ser un número entero.")
            return

        # 1. Buscar Cliente
        customer_obj = self.controller.data['customers'].get(email)
        if not customer_obj:
            messagebox.showerror("Error de Cliente", f"Cliente con email '{email}' no encontrado.")
            return

        # 2. Buscar Habitación
        room_obj = self.controller.data['rooms'].get(room_id)
        if not room_obj:
            messagebox.showerror("Error de Habitación", f"Habitación con ID '{room_id}' no existe.")
            return
        
        # 3. Validar que la habitación esté disponible
        if room_obj.getStatus() != "Available":
            messagebox.showerror("Habitación No Disponible", 
                                f"La Habitación {room_id} no está disponible. Por favor, seleccione otra.")
            return

        # 4. Crear Objeto Reservation
        new_res_id = self.controller.next_reservation_id
        
        reservation = Reservation(
            new_res_id,
            check_in_str,
            check_out_str,
            customer_obj,
            room_obj
        )

        # 5. Ejecutar la lógica POO y actualizar la base de datos
        if reservation.createReservation():
            self.controller.add_new_reservation(reservation)
            
            # Calcular costo total (número de noches * costo por noche)
            from datetime import datetime
            check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
            check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()
            num_nights = (check_out - check_in).days
            total_cost = room_obj.getCost() * num_nights
            
            # Abrir ventana de pago
            PaymentWindow(self.master, self.controller, reservation, total_cost, customer_obj)
            self.destroy()
        else:
            messagebox.showerror("Reserva Fallida", 
                                f"No se pudo crear la reserva en la Habitación {room_id}. Estado: {room_obj.getStatus()}")


# ----------------- Ventana de Pago (NUEVA) -----------------
class PaymentWindow(tk.Toplevel):
    """Ventana modal para procesar el pago de una reserva."""
    def __init__(self, master, controller, reservation, total_cost, customer):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.reservation = reservation
        self.total_cost = total_cost
        self.customer = customer
        
        self.title("Procesar Pago")
        self.geometry("500x450")
        self.resizable(False, False)
        self.configure(bg=PASTEL_BG)

        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="PROCESAMIENTO DE PAGO", style='Header.TLabel', foreground=PASTEL_HEADER).pack(pady=10)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=15, padx=10, fill="both", expand=True)
        
        # Información de la reserva
        ttk.Label(form_frame, text=f"Reserva #{reservation.getId()}:", font=('Arial', 11, 'bold')).pack(anchor="w", pady=5)
        ttk.Label(form_frame, text=f"Cliente: {customer.getName()}").pack(anchor="w")
        ttk.Label(form_frame, text=f"Habitación: {reservation._Reservation__room.getId()}").pack(anchor="w")
        ttk.Label(form_frame, text=f"Precio por noche: ${reservation._Reservation__room.getCost():.2f}").pack(anchor="w")
        
        # Separador
        ttk.Separator(form_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Monto total
        total_frame = ttk.Frame(form_frame)
        total_frame.pack(anchor="w", pady=10)
        ttk.Label(total_frame, text="TOTAL A PAGAR:", font=('Arial', 12, 'bold')).pack(anchor="w")
        ttk.Label(total_frame, text=f"${total_cost:.2f}", font=('Arial', 18, 'bold'), foreground=PASTEL_HEADER).pack(anchor="e", padx=20)
        
        # Método de pago
        ttk.Label(form_frame, text="Método de Pago:").pack(anchor="w", pady=(15, 5))
        self.payment_method_var = tk.StringVar(value="Tarjeta de Crédito")
        payment_methods = ["Tarjeta de Crédito", "Tarjeta de Débito", "Efectivo", "Transferencia Bancaria"]
        
        for method in payment_methods:
            ttk.Radiobutton(form_frame, text=method, variable=self.payment_method_var, value=method).pack(anchor="w")
        
        # Campo de referencia (opcional)
        ttk.Label(form_frame, text="Referencia/Número de Transacción (Opcional):").pack(anchor="w", pady=(15, 5))
        self.reference_entry = ttk.Entry(form_frame, width=50)
        self.reference_entry.pack(anchor="w")
        
        # Botones (apilados debajo del formulario)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20, fill='x')

        ttk.Button(button_frame, text="PAGAR", command=self.process_payment, 
               style='Access.TButton').pack(fill='x', pady=5)
        ttk.Button(button_frame, text="CANCELAR", command=self.destroy).pack(fill='x', pady=5)

    def process_payment(self):
        """Procesa el pago y lo registra en la base de datos."""
        payment_method = self.payment_method_var.get()
        
        # Importar Payment class
        from payment import Payment
        
        # Crear objeto Payment
        payment = Payment(
            self.controller.next_payment_id,
            self.total_cost,
            payment_method,
            self.reservation
        )
        
        # Procesar el pago
        payment.processPayment()
        
        # Agregar a la base de datos
        self.controller.add_new_payment(payment)
        
        # Mostrar confirmación
        messagebox.showinfo("Pago Exitoso", 
                           f"Pago de ${self.total_cost:.2f} procesado correctamente.\n"
                           f"Método: {payment_method}\n"
                           f"Reserva #{self.reservation.getId()} confirmada.")
        
        self.destroy()


# ----------------- Pantalla de Registro de Huésped (Clase anterior) -----------------
class RegisterCustomerWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Registro de Nuevo Huésped")
        self.geometry("600x550")
        self.resizable(False, False)
        self.configure(bg=PASTEL_BG)

        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="REGISTRO DE HUÉSPED", style='Header.TLabel', foreground=PASTEL_HEADER).pack(pady=10)
        
        canvas = tk.Canvas(main_frame, bg=PASTEL_BG, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.form_frame = ttk.Frame(canvas, padding="10")
        canvas.create_window((0, 0), window=self.form_frame, anchor="nw", tags="self.form_frame")

        self.form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        # Diccionario para almacenar las entradas
        self.entries = {}
        fields = [
            ("Primer Nombre:", "first_name"), ("Segundo Nombre (Opcional):", "middle_name"),
            ("Apellido Paterno:", "last_name"), ("Apellido Materno:", "second_last_name"),
            ("Teléfono:", "phone"), ("Email:", "email"),
            ("Estado (Ej: Querétaro):", "state"), ("CURP:", "curp")
        ]

        # Creación dinámica de campos
        for i, (label_text, key) in enumerate(fields):
            ttk.Label(self.form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=5, padx=5)
            entry = ttk.Entry(self.form_frame, width=40)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[key] = entry
        
        # Campos de contraseña
        pw_row = len(fields)
        ttk.Label(self.form_frame, text="Contraseña:").grid(row=pw_row, column=0, sticky="w", pady=5, padx=5)
        self.password_entry = ttk.Entry(self.form_frame, width=40, show="*")
        self.password_entry.grid(row=pw_row, column=1, pady=5, padx=5)

        ttk.Label(self.form_frame, text="Confirmar Contraseña:").grid(row=pw_row+1, column=0, sticky="w", pady=5, padx=5)
        self.confirm_password_entry = ttk.Entry(self.form_frame, width=40, show="*")
        self.confirm_password_entry.grid(row=pw_row+1, column=1, pady=5, padx=5)

        # Botones: Registrar y Regresar (apilados verticalmente)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20, fill='x')
        ttk.Button(btn_frame, text="REGISTRAR HUÉSPED", command=self.process_registration, 
                   style='Access.TButton').pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="REGRESAR", command=self.go_back).pack(fill='x', pady=5)

    def process_registration(self):
        """Recoge datos, valida y crea el nuevo objeto Customer."""
        
        data = {k: v.get().strip() for k, v in self.entries.items()}
        password = self.password_entry.get().strip()
        confirm_pw = self.confirm_password_entry.get().strip()
        
        # Validación simple de campos obligatorios
        required = ['first_name', 'last_name', 'phone', 'email', 'state', 'curp']
        if not all(data[key] for key in required):
            messagebox.showwarning("Datos Incompletos", "Por favor, complete todos los campos obligatorios.")
            return

        # Validación de Email simple
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            messagebox.showerror("Error de Formato", "El formato del email no es válido.")
            return
        
        # Validación de contraseña
        if not password:
            messagebox.showerror("Contraseña", "Por favor ingrese una contraseña.")
            return
        if password != confirm_pw:
            messagebox.showerror("Contraseña", "Las contraseñas no coinciden.")
            return
            
        # 1. Calcular nuevo ID para cliente basado en los objetos existentes
        try:
            existing_ids = [c.getId() for c in self.controller.data['customers'].values()]
            new_id = max(existing_ids) + 1 if existing_ids else 1
        except Exception:
            new_id = 1

        new_customer = Customer(
            id=new_id,
            name=data['first_name'],
            secondName=data['middle_name'],
            lastName=data['last_name'],
            secondLastName=data['second_last_name'],
            phone=data['phone'],
            email=data['email'],
            state=data['state'],
            curp=data['curp'],
            password=password
        )
        
        # 2. Registrar el cliente
        # new_customer.registerCustomer() # Ejecución de método POO
        self.controller.add_new_customer(new_customer)
        
        messagebox.showinfo("Registro Exitoso", f"Huésped {data['first_name']} {data['last_name']} registrado con éxito.")
        self.destroy()

    def go_back(self):
        """Cierra la ventana y regresa a la pantalla de bienvenida."""
        try:
            self.controller.show_frame("WelcomeScreen")
        except Exception:
            pass
        self.destroy()


# ----------------- Pantalla de Registro de Empleado (NUEVA) -----------------
class RegisterEmployeeWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Registro de Nuevo Empleado")
        self.geometry("600x520")
        self.resizable(False, False)
        self.configure(bg=PASTEL_BG)

        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="REGISTRO DE EMPLEADO", style='Header.TLabel', foreground=PASTEL_HEADER).pack(pady=10)
        
        canvas = tk.Canvas(main_frame, bg=PASTEL_BG, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.form_frame = ttk.Frame(canvas, padding="10")
        canvas.create_window((0, 0), window=self.form_frame, anchor="nw", tags="self.form_frame")

        self.form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Diccionario para almacenar las entradas
        self.entries = {}
        fields = [
            ("Primer Nombre:", "first_name"), ("Segundo Nombre (Opcional):", "middle_name"),
            ("Apellido Paterno:", "last_name"), ("Apellido Materno:", "second_last_name"),
            ("Teléfono:", "phone"), ("Email:", "email"),
            ("Estado (Activo/Inactivo):", "status"), ("CURP:", "curp")
        ]

        # Creación dinámica de campos
        for i, (label_text, key) in enumerate(fields):
            ttk.Label(self.form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=5, padx=5)
            entry = ttk.Entry(self.form_frame, width=40)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[key] = entry

        # Valor por defecto para status
        self.entries['status'].insert(0, 'Active')
        
        # Tipo de empleado (Recepcionista, Botones, Servicio)
        role_row = len(fields) + 0
        ttk.Label(self.form_frame, text="Tipo de Empleado:").grid(row=role_row, column=0, sticky="w", pady=5, padx=5)
        self.role_var = tk.StringVar(value="Recepcionista")
        role_combo = ttk.Combobox(self.form_frame, textvariable=self.role_var,
                                  values=["Recepcionista", "Botones", "Servicio"], state="readonly", width=37)
        role_combo.grid(row=role_row, column=1, pady=5, padx=5)
        
        # Campos de contraseña
        pw_row = len(fields)
        ttk.Label(self.form_frame, text="Contraseña:").grid(row=pw_row, column=0, sticky="w", pady=5, padx=5)
        self.password_entry = ttk.Entry(self.form_frame, width=40, show="*")
        self.password_entry.grid(row=pw_row, column=1, pady=5, padx=5)

        ttk.Label(self.form_frame, text="Confirmar Contraseña:").grid(row=pw_row+1, column=0, sticky="w", pady=5, padx=5)
        self.confirm_password_entry = ttk.Entry(self.form_frame, width=40, show="*")
        self.confirm_password_entry.grid(row=pw_row+1, column=1, pady=5, padx=5)

        # Botones: Registrar y Regresar (apilados verticalmente)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20, fill='x')
        ttk.Button(btn_frame, text="REGISTRAR EMPLEADO", command=self.process_registration, 
                   style='Access.TButton').pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="REGRESAR", command=self.go_back).pack(fill='x', pady=5)

    def process_registration(self):
        """Recoge datos, valida y crea el nuevo objeto Employee."""
        data = {k: v.get().strip() for k, v in self.entries.items()}
        password = self.password_entry.get().strip()
        confirm_pw = self.confirm_password_entry.get().strip()

        # Validación simple de campos obligatorios
        required = ['first_name', 'last_name', 'phone', 'email', 'status', 'curp']
        if not all(data[key] for key in required):
            messagebox.showwarning("Datos Incompletos", "Por favor, complete todos los campos obligatorios.")
            return

        # Validación de Email simple
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            messagebox.showerror("Error de Formato", "El formato del email no es válido.")
            return

        # Validación de contraseña
        if not password:
            messagebox.showerror("Contraseña", "Por favor ingrese una contraseña para el empleado.")
            return
        if password != confirm_pw:
            messagebox.showerror("Contraseña", "Las contraseñas no coinciden.")
            return

        # 1. Calcular nuevo ID para empleado
        try:
            existing_ids = [int(k) for k in self.controller.data['employees'].keys()]
            new_id = max(existing_ids) + 1 if existing_ids else 1
        except Exception:
            new_id = 1

        # 2. Crear objeto Employee
        # Crear la instancia del tipo adecuado según la selección
        role = getattr(self, 'role_var', None)
        selected_role = role.get() if role else 'Servicio'

        if selected_role == 'Recepcionista':
            new_employee = Receptionist(
                new_id,
                data['first_name'],
                data['middle_name'],
                data['last_name'],
                data['second_last_name'],
                data['phone'],
                data['email'],
                data['status'],
                data['curp'],
                password
            )
        elif selected_role == 'Botones':
            new_employee = Bellboy(
                new_id,
                data['first_name'],
                data['middle_name'],
                data['last_name'],
                data['second_last_name'],
                data['phone'],
                data['email'],
                data['status'],
                data['curp'],
                password
            )
        else:
            # Servicio u otros -> Employee genérico
            new_employee = Employee(
                new_id,
                data['first_name'],
                data['middle_name'],
                data['last_name'],
                data['second_last_name'],
                data['phone'],
                data['email'],
                data['status'],
                data['curp'],
                password
            )

        # 3. Registrar empleado en el controlador
        self.controller.add_new_employee(new_employee)

        messagebox.showinfo("Registro Exitoso", f"Empleado {data['first_name']} {data['last_name']} registrado con éxito.")
        self.destroy()

    def go_back(self):
        """Cierra la ventana y regresa a la pantalla de bienvenida."""
        try:
            self.controller.show_frame("WelcomeScreen")
        except Exception:
            pass
        self.destroy()

# ----------------- Inicio de la Aplicación -----------------
if __name__ == '__main__':
    root = tk.Tk()
    app = HotelGUI(root)
    root.mainloop()