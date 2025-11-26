import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
import re 
import uuid 

# Importar clases de POO (Asegúrate de que los archivos estén en la misma carpeta)
from customer import Customer
from service import Service 
from reservationService import ServiceReservation 
from reservation import Reservation 
from room import Room
from employee import Employee
from receptionist import Receptionist
from bellboy import Bellboy
from payment import Payment

# ----------------- PALETA DE COLORES Y ESTILOS (LUXURY THEME) -----------------
# Colores
COLOR_PRIMARY = '#1A237E'      # Azul Marino Profundo (Barra lateral/Encabezados)
COLOR_SECONDARY = '#283593'    # Azul un poco más claro (Hover)
COLOR_ACCENT = '#D4AF37'       # Dorado (Botones de acción principal)
COLOR_BG = '#F5F6FA'           # Gris muy claro (Fondo de la app)
COLOR_WHITE = '#FFFFFF'        # Blanco (Tarjetas)
COLOR_TEXT = '#2C3E50'         # Gris Oscuro (Texto principal)
COLOR_TEXT_LIGHT = '#7F8C8D'   # Gris Suave (Subtítulos)
COLOR_DANGER = '#C0392B'       # Rojo elegante (Errores/Cancelar)

# Fuentes
FONT_HEADER = ('Segoe UI', 20, 'bold')
FONT_SUBHEADER = ('Segoe UI', 14, 'bold')
FONT_BODY = ('Segoe UI', 10)
FONT_BODY_BOLD = ('Segoe UI', 10, 'bold')
FONT_BUTTON = ('Segoe UI', 10, 'bold')

# ----------------- Funciones de Inicialización de Datos -----------------
# (Misma lógica que tu archivo original, sin cambios funcionales)
def init_data():
    customer1 = Customer(1, "Andrea", "Sarahi", "Lopez", "Guerrero", "4420000000", "andrea@mail.com", "Querétaro", "LOGA001122QRO", password="andrea123")
    customer2 = Customer(2, "Juan", "", "Perez", "Vera", "4423333333", "juan@mail.com", "Querétaro", "PEVJ001122QRO", password="juan123")
    receptionist = Receptionist(1, "Brigitte", "", "Herrera", "Rodriguez", "4421111111", "brigitte@mail.com", "Active", "HERB001122QRO", password="brigitte123")
    
    rooms = {}
    room_types = ["Suite", "Doble", "Individual"]
    room_costs = {"Suite": 1500.0, "Doble": 900.0, "Individual": 600.0}
    
    import random
    random.seed(42)
    
    for i in range(100):
        room_id = 101 + i
        room_type = room_types[i % 3]
        cost = room_costs[room_type]
        status = "Not available" if random.random() < 0.2 else "Available"
        description = f"{room_type} room with capacity for {2 if room_type == 'Individual' else 4} persons"
        rooms[room_id] = Room(room_id, room_type, status, cost, description)
    
    service1 = Service(1, "Desayuno a la Habitación", 150.0, "Desayuno continental.")
    service2 = Service(2, "Lavandería Express", 200.0, "Lavado en < 3 horas.")
    service3 = Service(3, "Masaje Relajante", 500.0, "Sesión de 60 min.")
    
    reservation1 = Reservation(1, "2025-10-10", "2025-10-15", customer1, rooms[103], None)
    rooms[103].setStatus("Not available") 
    customer1.makeReservation(reservation1)
    
    service_reservation1 = ServiceReservation(101, "2025-10-11 08:00", customer1, service1)
    customer1.makeServiceReservation(service_reservation1)
    
    service_reservation2 = ServiceReservation(102, "2025-10-12 12:30", customer2, service3)
    customer2.makeServiceReservation(service_reservation2)
    
    return {
        'customers': {c.getEmail(): c for c in [customer1, customer2]}, 
        'employees': {'1': receptionist}, 
        'rooms': rooms,
        'reservations': {1: reservation1},
        'service_reservations': {101: service_reservation1, 102: service_reservation2},
        'services': {s.getId(): s for s in [service1, service2, service3]}
    }

# ----------------- Utilidades UI -----------------

def center_window(window, width, height):
    """Centra la ventana en la pantalla."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (width/2))
    y_cordinate = int((screen_height/2) - (height/2))
    window.geometry(f"{width}x{height}+{x_cordinate}+{y_cordinate}")

class ModernButton(tk.Button):
    """Botón personalizado plano y moderno."""
    def __init__(self, master, text, command, type="primary", **kwargs):
        bg = COLOR_PRIMARY if type == "primary" else (COLOR_ACCENT if type == "accent" else COLOR_WHITE)
        fg = COLOR_WHITE if type in ["primary", "accent"] else COLOR_PRIMARY
        
        super().__init__(master, text=text, command=command, 
                         bg=bg, fg=fg, 
                         font=FONT_BUTTON, relief="flat", 
                         activebackground=COLOR_SECONDARY, activeforeground=COLOR_WHITE,
                         bd=0, padx=20, pady=10, cursor="hand2", **kwargs)

# ----------------- Clase Controladora de la Aplicación -----------------

class HotelGUI:
    def __init__(self, master):
        self.master = master
        master.title("🏨 Le Villa Hotel Management")
        master.configure(bg=COLOR_BG)
        center_window(master, 900, 600)
        
        # Configuración de estilos TTK global
        self.style = ttk.Style()
        self.style.theme_use('clam') # 'clam' permite más personalización de colores que 'vista' o 'default'
        
        # Configurar colores de Frames y Labels
        self.style.configure('TFrame', background=COLOR_BG)
        self.style.configure('Card.TFrame', background=COLOR_WHITE, relief="groove", borderwidth=1)
        
        self.style.configure('TLabel', background=COLOR_BG, foreground=COLOR_TEXT, font=FONT_BODY)
        self.style.configure('Card.TLabel', background=COLOR_WHITE, foreground=COLOR_TEXT, font=FONT_BODY)
        self.style.configure('Header.TLabel', font=FONT_HEADER, foreground=COLOR_PRIMARY, background=COLOR_BG)
        self.style.configure('Title.TLabel', font=FONT_SUBHEADER, foreground=COLOR_PRIMARY, background=COLOR_WHITE)
        
        # Configurar Entradas
        self.style.configure('TEntry', padding=5, relief="flat", borderwidth=1)
        self.style.map('TEntry', bordercolor=[('focus', COLOR_PRIMARY)])

        self.container = ttk.Frame(master)
        self.container.pack(fill="both", expand=True)
        
        self.data = init_data()
        
        self.next_reservation_id = max(self.data['reservations'].keys()) + 1 if self.data['reservations'] else 1
        self.next_service_reservation_id = max(self.data['service_reservations'].keys()) + 1 if self.data['service_reservations'] else 1
        self.next_payment_id = 1
        self.data['payments'] = {}
        
        self.frames = {}

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
        
    # Métodos de lógica (add_new...) se mantienen idénticos para no romper funcionalidad
    def add_new_reservation(self, new_reservation):
        res_id = self.next_reservation_id
        self.data['reservations'][res_id] = new_reservation
        self.next_reservation_id += 1
        return res_id

    def add_new_service_reservation(self, new_service_reservation):
        res_id = self.next_service_reservation_id
        self.data['service_reservations'][res_id] = new_service_reservation
        self.next_service_reservation_id += 1
        return res_id

    def add_new_customer(self, customer_obj):
        self.data['customers'][customer_obj.getEmail()] = customer_obj
        return customer_obj

    def add_new_employee(self, employee_obj):
        key = str(employee_obj.getId())
        self.data['employees'][key] = employee_obj
        return employee_obj

    def add_new_payment(self, payment_obj):
        pay_id = self.next_payment_id
        self.data['payments'][pay_id] = payment_obj
        self.next_payment_id += 1
        return payment_obj

# ----------------- Clases de Ventanas Modales (Mejoradas) -----------------

class CreateServiceReservationWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Solicitar Nuevo Servicio")
        center_window(self, 500, 600)
        self.configure(bg=COLOR_BG)

        # Contenedor principal estilo Tarjeta
        card = ttk.Frame(self, style='Card.TFrame', padding=20)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(card, text="🛎️ Solicitar Servicio", style='Title.TLabel').pack(pady=(0, 20))
        
        # Formulario
        form_frame = ttk.Frame(card, style='Card.TFrame')
        form_frame.pack(fill='both', expand=True)

        ttk.Label(form_frame, text="Email del Cliente", style='Card.TLabel', font=FONT_BODY_BOLD).pack(anchor='w')
        self.email_entry = ttk.Entry(form_frame, width=40)
        self.email_entry.pack(fill='x', pady=(5, 15))
        
        if controller.frames['MainMenuScreen'].user_type == 'Customer' and controller.frames['MainMenuScreen'].user_obj:
            self.email_entry.insert(0, controller.frames['MainMenuScreen'].user_obj.getEmail())
            self.email_entry.config(state='readonly')
        else:
            self.email_entry.insert(0, "andrea@mail.com")

        ttk.Label(form_frame, text="Habitación (Opcional)", style='Card.TLabel', font=FONT_BODY_BOLD).pack(anchor='w')
        self.room_number_entry = ttk.Entry(form_frame, width=40)
        self.room_number_entry.pack(fill='x', pady=(5, 15))
        self.room_number_entry.insert(0, "101")

        ttk.Label(form_frame, text="Servicio", style='Card.TLabel', font=FONT_BODY_BOLD).pack(anchor='w')
        self.services = self.controller.data['services']
        service_options = [f"{s.getId()}: {s.getType()} (${s.getCost():.2f})" for s in self.services.values()]
        
        self.service_var = tk.StringVar(form_frame)
        self.service_combo = ttk.Combobox(form_frame, textvariable=self.service_var, values=service_options, state="readonly")
        self.service_combo.pack(fill='x', pady=(5, 15))
        if service_options: self.service_combo.set(service_options[0])

        ttk.Label(form_frame, text="Fecha/Hora (AAAA-MM-DD HH:MM)", style='Card.TLabel', font=FONT_BODY_BOLD).pack(anchor='w')
        self.datetime_entry = ttk.Entry(form_frame, width=40)
        self.datetime_entry.pack(fill='x', pady=(5, 20))
        self.datetime_entry.insert(0, str(date.today()) + " 10:00")
        
        # Botones
        ModernButton(card, text="CONFIRMAR SOLICITUD", type="accent", command=self.process_service_reservation).pack(fill='x', pady=5)
        ModernButton(card, text="CANCELAR", type="secondary", command=self.destroy).pack(fill='x', pady=5)

    def validate_datetime(self, dt_str):
        return re.match(r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}$', dt_str)

    def process_service_reservation(self):
        email = self.email_entry.get().strip()
        room_number = self.room_number_entry.get().strip()
        service_info = self.service_var.get().strip()
        date_time_str = self.datetime_entry.get().strip()

        if not all([email, service_info, date_time_str]):
            messagebox.showwarning("Faltan Datos", "Complete todos los campos.")
            return
        
        if not self.validate_datetime(date_time_str):
            messagebox.showerror("Error", "Formato de fecha inválido.")
            return

        customer_obj = self.controller.data['customers'].get(email)
        if not customer_obj:
            messagebox.showerror("Error", "Cliente no encontrado.")
            return

        try:
            service_id = int(service_info.split(':')[0])
            service_obj = self.services.get(service_id)
        except:
            return

        new_res_id = self.controller.next_service_reservation_id
        reservation = ServiceReservation(new_res_id, date_time_str, customer_obj, service_obj)

        if reservation.createReservation():
            self.controller.add_new_service_reservation(reservation)
            PaymentServiceWindow(self.master, self.controller, reservation, service_obj.getCost(), customer_obj, room_number)
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear la reserva.")


class PaymentServiceWindow(tk.Toplevel):
    def __init__(self, master, controller, reservation, service_cost, customer, room_number):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.reservation = reservation
        self.service_cost = service_cost
        
        self.title("Pasarela de Pago")
        center_window(self, 450, 550)
        self.configure(bg=COLOR_BG)

        card = ttk.Frame(self, style='Card.TFrame', padding=25)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(card, text="💳 Detalles del Pago", style='Title.TLabel').pack(pady=(0, 20))
        
        info_frame = ttk.Frame(card, style='Card.TFrame')
        info_frame.pack(fill='x', pady=10)
        
        # Resumen
        ttk.Label(info_frame, text=f"Servicio: {reservation._ServiceReservation__service.getType()}", style='Card.TLabel').pack(anchor='w')
        ttk.Label(info_frame, text=f"Cliente: {customer.getName()}", style='Card.TLabel').pack(anchor='w')
        
        ttk.Separator(card, orient='horizontal').pack(fill='x', pady=15)
        
        # Total
        ttk.Label(card, text="TOTAL A PAGAR", style='Card.TLabel', font=('Segoe UI', 10)).pack()
        ttk.Label(card, text=f"${service_cost:.2f}", style='Card.TLabel', font=('Segoe UI', 24, 'bold'), foreground=COLOR_PRIMARY).pack(pady=5)
        
        # Método
        ttk.Label(card, text="Método de Pago:", style='Card.TLabel', font=FONT_BODY_BOLD).pack(anchor='w', pady=(15, 5))
        self.payment_method_var = tk.StringVar(value="Tarjeta de Crédito")
        
        # Estilo para radio buttons
        s = ttk.Style()
        s.configure('TRadiobutton', background=COLOR_WHITE, font=FONT_BODY)
        
        ttk.Radiobutton(card, text="💳 Tarjeta de Crédito", variable=self.payment_method_var, value="Tarjeta de Crédito").pack(anchor='w')
        ttk.Radiobutton(card, text="💵 Efectivo", variable=self.payment_method_var, value="Efectivo").pack(anchor='w')
        
        ModernButton(card, text="PAGAR AHORA", type="accent", command=self.process_payment).pack(fill='x', pady=(30, 5))
        ModernButton(card, text="CANCELAR", type="secondary", command=self.destroy).pack(fill='x', pady=5)

    def process_payment(self):
        payment = Payment(
            self.controller.next_payment_id,
            self.service_cost,
            self.payment_method_var.get(),
            self.reservation
        )
        payment.processPayment()
        self.controller.add_new_payment(payment)
        messagebox.showinfo("Pago Exitoso", "El pago ha sido procesado correctamente.")
        self.destroy()

# ----------------- Pantallas Principales -----------------

class WelcomeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Fondo decorativo lateral o superior (simulado con Frames)
        header = tk.Frame(self, bg=COLOR_PRIMARY, height=150)
        header.pack(fill='x')
        
        title = tk.Label(header, text="LE VILLA", font=('Times New Roman', 40, 'bold'), bg=COLOR_PRIMARY, fg=COLOR_ACCENT)
        title.place(relx=0.5, rely=0.5, anchor='center')
        
        subtitle = tk.Label(header, text="HOTEL & SPA", font=('Segoe UI', 12, 'bold'), bg=COLOR_PRIMARY, fg=COLOR_WHITE)
        subtitle.place(relx=0.5, rely=0.75, anchor='center')
        
        # Contenido
        content = tk.Frame(self, bg=COLOR_BG)
        content.pack(fill='both', expand=True, padx=50, pady=30)
        
        tk.Label(content, text="Seleccione su perfil de acceso", font=FONT_SUBHEADER, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=20)
        
        btn_container = tk.Frame(content, bg=COLOR_BG)
        btn_container.pack()
        
        # Botones Grandes
        ModernButton(btn_container, text="👤  ACCESO HUÉSPED", type="primary", 
                     command=lambda: controller.show_frame("LoginFormScreen", login_type="Customer")).grid(row=0, column=0, padx=10, pady=10)
        
        ModernButton(btn_container, text="👔  ACCESO EMPLEADO", type="primary",
                     command=lambda: controller.show_frame("LoginFormScreen", login_type="Employee")).grid(row=0, column=1, padx=10, pady=10)
        
        # Separador
        tk.Frame(content, height=1, bg="#DDDDDD", width=300).pack(pady=20)
        
        reg_frame = tk.Frame(content, bg=COLOR_BG)
        reg_frame.pack()
        
        tk.Button(reg_frame, text="Crear cuenta Huésped", font=('Segoe UI', 9, 'underline'), 
                  bg=COLOR_BG, fg=COLOR_TEXT, bd=0, cursor="hand2",
                  command=lambda: RegisterCustomerWindow(controller.master, controller)).pack(side="left", padx=20)
                  
        tk.Button(reg_frame, text="Registrar Empleado", font=('Segoe UI', 9, 'underline'),
                  bg=COLOR_BG, fg=COLOR_TEXT, bd=0, cursor="hand2",
                  command=lambda: RegisterEmployeeWindow(controller.master, controller)).pack(side="left", padx=20)


class LoginFormScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Simplified layout: full-width form without the blue side panel
        right_panel = tk.Frame(self, bg=COLOR_BG)
        right_panel.pack(fill='both', expand=True, padx=50, pady=30)

        center_frame = tk.Frame(right_panel, bg=COLOR_BG)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        self.title_label = tk.Label(center_frame, text="INICIAR SESIÓN", font=FONT_HEADER, bg=COLOR_BG, fg=COLOR_PRIMARY)
        self.title_label.pack(pady=(0, 30), anchor='w')
        
        tk.Label(center_frame, text="Email", font=FONT_BODY_BOLD, bg=COLOR_BG, fg=COLOR_TEXT).pack(anchor='w')
        self.email_entry = ttk.Entry(center_frame, width=35)
        self.email_entry.pack(pady=(5, 15))
        
        tk.Label(center_frame, text="Contraseña", font=FONT_BODY_BOLD, bg=COLOR_BG, fg=COLOR_TEXT).pack(anchor='w')
        self.password_entry = ttk.Entry(center_frame, width=35, show="*")
        self.password_entry.pack(pady=(5, 25))
        
        ModernButton(center_frame, text="INGRESAR", type="accent", command=self.login).pack(fill='x', pady=5)
        ModernButton(center_frame, text="VOLVER", type="secondary", command=lambda: controller.show_frame("WelcomeScreen")).pack(fill='x', pady=5)

    def set_login_type(self, login_type):
        self.login_type = login_type
        if login_type == "Customer":
            self.title_label.config(text="ACCESO HUÉSPED")
            self.email_entry.delete(0, tk.END); self.email_entry.insert(0, "andrea@mail.com")
        else: 
            self.title_label.config(text="ACCESO EMPLEADO")
            self.email_entry.delete(0, tk.END); self.email_entry.insert(0, "brigitte@mail.com")

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if self.login_type == "Customer":
            user_obj = self.controller.data['customers'].get(email)
            if user_obj and user_obj.getPassword() == password:
                self.controller.show_frame("MainMenuScreen", user_type="Customer", user_obj=user_obj)
            else:
                messagebox.showerror("Error", "Credenciales inválidas.")
        else: 
            user_obj = next((emp for emp in self.controller.data['employees'].values() if getattr(emp, 'getEmail', lambda: None)() == email), None)
            if user_obj and user_obj.getPassword() == password:
                self.controller.show_frame("MainMenuScreen", user_type="Employee", user_obj=user_obj)
            else:
                messagebox.showerror("Error", "Credenciales inválidas.")


class LoginSuccessScreen(ttk.Frame):
    # Clase auxiliar para redirección, generalmente saltamos directo al menú
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
class MainMenuScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Barra Superior
        top_bar = tk.Frame(self, bg=COLOR_WHITE, height=60)
        top_bar.pack(side='top', fill='x')
        top_bar.pack_propagate(False)
        
        tk.Label(top_bar, text="LE VILLA DASHBOARD", font=('Times New Roman', 14, 'bold'), bg=COLOR_WHITE, fg=COLOR_PRIMARY).pack(side='left', padx=20)
        self.user_label = tk.Label(top_bar, text="", font=FONT_BODY, bg=COLOR_WHITE, fg=COLOR_TEXT)
        self.user_label.pack(side='right', padx=20)
        
        # Contenedor Principal con Scroll si fuera necesario, aqui usaremos grid simple
        self.main_area = tk.Frame(self, bg=COLOR_BG)
        self.main_area.pack(fill='both', expand=True, padx=40, pady=40)
        
        self.grid_buttons_frame = tk.Frame(self.main_area, bg=COLOR_BG)
        self.grid_buttons_frame.pack(anchor='center')

    def create_dashboard_card(self, parent, icon, title, command, row, col):
        """Crea un botón grande estilo tarjeta."""
        frame = tk.Frame(parent, bg=COLOR_WHITE, width=200, height=150)
        frame.grid(row=row, column=col, padx=15, pady=15)
        frame.pack_propagate(False) # Forzar tamaño
        
        # Comportamiento de botón en todo el frame
        def on_click(e): command()
        
        icon_lbl = tk.Label(frame, text=icon, font=('Segoe UI', 30), bg=COLOR_WHITE, fg=COLOR_PRIMARY, cursor="hand2")
        icon_lbl.pack(expand=True)
        icon_lbl.bind("<Button-1>", on_click)
        
        txt_lbl = tk.Label(frame, text=title, font=('Segoe UI', 11, 'bold'), bg=COLOR_WHITE, fg=COLOR_TEXT, cursor="hand2")
        txt_lbl.pack(pady=(0, 20))
        txt_lbl.bind("<Button-1>", on_click)
        
        frame.bind("<Button-1>", on_click)

    def set_user(self, user_type, user_obj):
        self.user_type = user_type
        self.user_obj = user_obj
        
        role_text = "Huésped" if user_type == "Customer" else "Empleado"
        name = user_obj.getName() if user_type == "Customer" else user_obj.getFirstName()
        self.user_label.config(text=f"{role_text}: {name} | 🔴 Cerrar Sesión")
        self.user_label.bind("<Button-1>", lambda e: self.controller.show_frame("WelcomeScreen"))
        self.user_label.configure(cursor="hand2")

        # Limpiar botones anteriores
        for widget in self.grid_buttons_frame.winfo_children():
            widget.destroy()

        # Generar Dashboard
        # Fila 1
        self.create_dashboard_card(self.grid_buttons_frame, "📅", "Reservar Habitación", self.open_create_reservation, 0, 0)
        self.create_dashboard_card(self.grid_buttons_frame, "🛎️", "Solicitar Servicio", self.open_create_service_reservation, 0, 1)
        self.create_dashboard_card(self.grid_buttons_frame, "👁️", "Ver Mis Reservas", self.view_room_reservation, 0, 2)
        
        # Fila 2
        self.create_dashboard_card(self.grid_buttons_frame, "🍽️", "Ver Servicios Activos", self.view_service_reservation, 1, 0)
        self.create_dashboard_card(self.grid_buttons_frame, "ℹ️", "Info Hab. Demo", self.view_room_info, 1, 1)
        
        # Opciones extra para pruebas
        self.create_dashboard_card(self.grid_buttons_frame, "🧪", "Test Pago (Última)", self.open_last_payment, 1, 2)

    # --- Wrappers de Funcionalidad ---
    def open_create_reservation(self): CreateReservationWindow(self.controller.master, self.controller)
    def open_create_service_reservation(self): CreateServiceReservationWindow(self.controller.master, self.controller)
    
    def view_room_reservation(self):
        # Abrir ventana estilizada de visualización de reservas
        ViewReservationsWindow(self.controller.master, self.controller)

    def view_service_reservation(self):
        # Abrir ventana estilizada de visualización de servicios
        ViewServicesWindow(self.controller.master, self.controller)

    def view_room_info(self):
        # Abrir ventana con información de habitaciones
        RoomInfoWindow(self.controller.master, self.controller)

    def open_last_payment(self):
        if not self.controller.data['reservations']: return
        last_id = max(self.controller.data['reservations'].keys())
        reservation = self.controller.data['reservations'][last_id]
        PaymentWindow(self.controller.master, self.controller, reservation, reservation.getRoom().getCost(), reservation.getCustomer())


# ----------------- Ventanas de Registro y Pago (Estilizadas) -----------------
# Versiones simplificadas con el nuevo estilo visual

class CreateReservationWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Reservar Habitación")
        center_window(self, 600, 700)
        self.configure(bg=COLOR_BG)
        
        container = ttk.Frame(self, style='Card.TFrame', padding=20)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(container, text="Nueva Reserva", style='Title.TLabel').pack(pady=(0, 20))

        # Grid layout para formulario
        f = ttk.Frame(container, style='Card.TFrame')
        f.pack(fill='both', expand=True)

        # Campos
        self.create_field(f, "Email Cliente:", 0)
        self.email_entry = ttk.Entry(f, width=30); self.email_entry.grid(row=0, column=1, pady=10)
        if controller.frames['MainMenuScreen'].user_type == 'Customer':
            self.email_entry.insert(0, controller.frames['MainMenuScreen'].user_obj.getEmail())

        self.create_field(f, "Tipo Habitación:", 1)
        self.room_type_var = tk.StringVar(value="Suite")
        self.cb_type = ttk.Combobox(f, textvariable=self.room_type_var, values=["Suite", "Doble", "Individual"], state="readonly")
        self.cb_type.grid(row=1, column=1, pady=10)
        
        self.create_field(f, "Check-In (AAAA-MM-DD):", 2)
        self.in_entry = ttk.Entry(f); self.in_entry.insert(0, str(date.today())); self.in_entry.grid(row=2, column=1, pady=10)

        self.create_field(f, "Check-Out (AAAA-MM-DD):", 3)
        self.out_entry = ttk.Entry(f); self.out_entry.insert(0, "2025-12-31"); self.out_entry.grid(row=3, column=1, pady=10)

        # Simulación simple de disponibilidad (sin lista completa para ahorrar espacio visual)
        self.create_field(f, "Habitación ID:", 4)
        self.room_id_entry = ttk.Entry(f); self.room_id_entry.insert(0, "101"); self.room_id_entry.grid(row=4, column=1, pady=10)
        
        # Agregar opción de servicio adicional
        ttk.Label(f, text="Servicio Adicional:", style='Card.TLabel', font=FONT_BODY_BOLD).grid(row=5, column=0, sticky='w', padx=10)
        services = controller.data.get('services', {})
        service_options = ["Ninguno"] + [f"{s.getId()}: {s.getType()} (${s.getCost():.2f})" for s in services.values()]
        self.service_var = tk.StringVar(value="Ninguno")
        self.service_cb = ttk.Combobox(f, textvariable=self.service_var, values=service_options, state='readonly')
        self.service_cb.grid(row=5, column=1, pady=10)

        ModernButton(container, text="CONFIRMAR RESERVA", type="primary", command=self.process).pack(fill='x', pady=(10,8))
        ModernButton(container, text="REGRESAR", type="secondary", command=self.destroy).pack(fill='x', pady=(0,10))

    def create_field(self, parent, text, row):
        ttk.Label(parent, text=text, style='Card.TLabel', font=FONT_BODY_BOLD).grid(row=row, column=0, sticky='w', padx=10)

    def process(self):
        # Lógica simplificada invocando la lógica original si es posible
        # Validar entradas antes de crear la reserva
        try:
            rid = int(self.room_id_entry.get())
        except Exception:
            messagebox.showerror("Error", "ID de habitación inválido.")
            return

        room = self.controller.data['rooms'].get(rid)
        cust = self.controller.data['customers'].get(self.email_entry.get())

        if not room or not cust:
            messagebox.showerror("Error", "Datos inválidos: cliente o habitación no encontrados.")
            return

        # Validar formato y orden de fechas
        from datetime import datetime
        try:
            check_in = datetime.strptime(self.in_entry.get().strip(), "%Y-%m-%d").date()
            check_out = datetime.strptime(self.out_entry.get().strip(), "%Y-%m-%d").date()
        except Exception:
            messagebox.showerror("Fecha inválida", "Formato de fecha inválido. Use AAAA-MM-DD.")
            return

        if check_out <= check_in:
            messagebox.showerror("Fechas inválidas", "La fecha de salida debe ser posterior a la fecha de entrada.")
            return

        # Crear reserva y proceder
        try:
            res = Reservation(self.controller.next_reservation_id, self.in_entry.get().strip(), self.out_entry.get().strip(), cust, room)
            if not res.createReservation():
                messagebox.showerror("Error", "Habitación no disponible.")
                return

            # Añadir reserva al controlador
            self.controller.add_new_reservation(res)

            # Calcular noches y subtotales
            num_nights = (check_out - check_in).days
            room_subtotal = room.getCost() * num_nights

            # Revisar servicio adicional
            additional_service = None
            service_subtotal = 0
            sel = self.service_var.get()
            svc_dict = self.controller.data.get('services', {})
            if sel and sel != "Ninguno":
                try:
                    sid = int(sel.split(':')[0])
                    additional_service = svc_dict.get(sid)
                    if additional_service:
                        service_subtotal = additional_service.getCost()
                except Exception:
                    additional_service = None

            total_cost = room_subtotal + service_subtotal

            PaymentWindow(self.master, self.controller, res, total_cost, cust, additional_service, room_subtotal, service_subtotal)
            self.destroy()
        except Exception:
            messagebox.showerror("Error", "Error procesando datos.")


class PaymentWindow(tk.Toplevel):
    def __init__(self, master, controller, reservation, total_cost, customer, additional_service=None, room_subtotal=None, service_subtotal=0):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.reservation = reservation
        self.total_cost = total_cost
        self.room_subtotal = room_subtotal
        self.service_subtotal = service_subtotal
        self.additional_service = additional_service
        
        self.title("Check-out y Pago")
        center_window(self, 400, 420)
        self.configure(bg=COLOR_BG)
        
        card = ttk.Frame(self, style='Card.TFrame', padding=20)
        card.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(card, text="Pago de Habitación", style='Title.TLabel').pack(pady=10)

        # Intentar calcular/desplegar subtotales si no se recibieron
        if self.room_subtotal is None:
            try:
                from datetime import datetime
                check_in = datetime.strptime(self.reservation.getCheckIn(), "%Y-%m-%d").date()
                check_out = datetime.strptime(self.reservation.getCheckOut(), "%Y-%m-%d").date()
                nights = (check_out - check_in).days
                self.room_subtotal = self.reservation.getRoom().getCost() * max(1, nights)
            except Exception:
                self.room_subtotal = self.total_cost

        # Mostrar desglose
        ttk.Label(card, text=f"Habitación: ${self.room_subtotal:.2f}", style='Card.TLabel').pack(pady=(8,2))
        if self.additional_service and self.service_subtotal:
            try:
                svc_name = self.additional_service.getType()
            except Exception:
                svc_name = 'Servicio'
            ttk.Label(card, text=f"{svc_name}: ${self.service_subtotal:.2f}", style='Card.TLabel').pack(pady=(0,4))

        ttk.Label(card, text=f"Total: ${self.total_cost:.2f}", font=('Segoe UI', 20, 'bold'), foreground=COLOR_PRIMARY, background=COLOR_WHITE).pack(pady=12)

        self.method = tk.StringVar(value="Tarjeta")
        ttk.Radiobutton(card, text="Tarjeta", variable=self.method, value="Tarjeta").pack()
        ttk.Radiobutton(card, text="Efectivo", variable=self.method, value="Efectivo").pack()

        # Botones: pagar y regresar
        btn_frame = ttk.Frame(card)
        btn_frame.pack(fill='x', pady=(12,0))
        ModernButton(btn_frame, text="PAGAR", command=self.pay).pack(side='left', fill='x', expand=True, padx=(0,6))
        ModernButton(btn_frame, text="REGRESAR", type='secondary', command=self.destroy).pack(side='right', fill='x', expand=True, padx=(6,0))
        
    def pay(self):
        p = Payment(self.controller.next_payment_id, self.total_cost, self.method.get(), self.reservation)
        p.processPayment()
        self.controller.add_new_payment(p)
        messagebox.showinfo("Éxito", "Pago completado.")
        self.destroy()


class ViewReservationsWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Reservas")
        center_window(self, 600, 420)
        self.configure(bg=COLOR_BG)

        card = ttk.Frame(self, style='Card.TFrame', padding=20)
        card.pack(fill='both', expand=True, padx=20, pady=20)
        ttk.Label(card, text="Reservas", style='Title.TLabel').pack(pady=(0,10))

        text_frame = ttk.Frame(card, style='Card.TFrame')
        text_frame.pack(fill='both', expand=True)

        txt = tk.Text(text_frame, wrap='word', bg=COLOR_WHITE, fg=COLOR_TEXT)
        txt.pack(side='left', fill='both', expand=True)
        sb = ttk.Scrollbar(text_frame, orient='vertical', command=txt.yview)
        sb.pack(side='right', fill='y')
        txt.configure(yscrollcommand=sb.set)

        # Cargar reservas según rol
        if controller.frames.get('MainMenuScreen') and controller.frames['MainMenuScreen'].user_type == 'Employee':
            reservations = list(controller.data.get('reservations', {}).values())
        else:
            user = controller.frames.get('MainMenuScreen') and controller.frames['MainMenuScreen'].user_obj
            reservations = user.getReservations() if user else []

        if not reservations:
            txt.insert('end', 'No hay reservas para mostrar.')
        else:
            for r in reservations:
                try:
                    txt.insert('end', r.showInfo() + '\n' + ('-'*60) + '\n')
                except Exception:
                    txt.insert('end', str(r) + '\n' + ('-'*60) + '\n')

        txt.config(state='disabled')

        ModernButton(card, text="REGRESAR", type='secondary', command=self.destroy).pack(fill='x', pady=10)


class ViewServicesWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Servicios Activos")
        center_window(self, 600, 420)
        self.configure(bg=COLOR_BG)

        card = ttk.Frame(self, style='Card.TFrame', padding=20)
        card.pack(fill='both', expand=True, padx=20, pady=20)
        ttk.Label(card, text="Servicios Activos", style='Title.TLabel').pack(pady=(0,10))

        text_frame = ttk.Frame(card, style='Card.TFrame')
        text_frame.pack(fill='both', expand=True)

        txt = tk.Text(text_frame, wrap='word', bg=COLOR_WHITE, fg=COLOR_TEXT)
        txt.pack(side='left', fill='both', expand=True)
        sb = ttk.Scrollbar(text_frame, orient='vertical', command=txt.yview)
        sb.pack(side='right', fill='y')
        txt.configure(yscrollcommand=sb.set)

        if controller.frames.get('MainMenuScreen') and controller.frames['MainMenuScreen'].user_type == 'Employee':
            services = list(controller.data.get('service_reservations', {}).values())
        else:
            user = controller.frames.get('MainMenuScreen') and controller.frames['MainMenuScreen'].user_obj
            services = user.getServiceReservations() if user else []

        if not services:
            txt.insert('end', 'No hay servicios activos para mostrar.')
        else:
            for s in services:
                try:
                    txt.insert('end', s.showInfo() + '\n' + ('-'*60) + '\n')
                except Exception:
                    txt.insert('end', str(s) + '\n' + ('-'*60) + '\n')

        txt.config(state='disabled')

        ModernButton(card, text="REGRESAR", type='secondary', command=self.destroy).pack(fill='x', pady=10)


class RoomInfoWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Información de Habitaciones")
        center_window(self, 600, 420)
        self.configure(bg=COLOR_BG)

        card = ttk.Frame(self, style='Card.TFrame', padding=20)
        card.pack(fill='both', expand=True, padx=20, pady=20)
        ttk.Label(card, text="Información de Habitaciones", style='Title.TLabel').pack(pady=(0,10))

        tree_frame = ttk.Frame(card)
        tree_frame.pack(fill='both', expand=True)

        txt = tk.Text(tree_frame, wrap='none', bg=COLOR_WHITE, fg=COLOR_TEXT)
        txt.pack(side='left', fill='both', expand=True)
        sb = ttk.Scrollbar(tree_frame, orient='vertical', command=txt.yview)
        sb.pack(side='right', fill='y')
        txt.configure(yscrollcommand=sb.set)

        rooms = controller.data.get('rooms', {}).values()
        if not rooms:
            txt.insert('end', 'No hay información de habitaciones.')
        else:
            for r in sorted(rooms, key=lambda x: x.getId()):
                info = f"ID: {r.getId()} | Tipo: {r.getType()} | Precio: ${r.getCost():.2f} | Estado: {r.getStatus()}\n"
                txt.insert('end', info)

        txt.config(state='disabled')

        ModernButton(card, text="REGRESAR", type='secondary', command=self.destroy).pack(fill='x', pady=10)


class RegisterCustomerWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Registro Cliente")
        center_window(self, 500, 600)
        self.configure(bg=COLOR_BG)
        
        # Implementación visual simplificada para consistencia
        c = ttk.Frame(self, style='Card.TFrame', padding=20); c.pack(fill='both', expand=True, padx=20, pady=20)
        ttk.Label(c, text="Nuevo Huésped", style='Title.TLabel').pack()
        
        f = ttk.Frame(c, style='Card.TFrame'); f.pack(pady=10)
        
        self.entries = {}
        fields = ["first_name", "last_name", "email", "phone", "state", "curp"]
        for i, field in enumerate(fields):
            ttk.Label(f, text=field.capitalize(), style='Card.TLabel').grid(row=i, column=0, sticky='w')
            e = ttk.Entry(f); e.grid(row=i, column=1, pady=5); self.entries[field] = e
            
        ttk.Label(f, text="Password", style='Card.TLabel').grid(row=6, column=0)
        self.pw = ttk.Entry(f, show="*"); self.pw.grid(row=6, column=1, pady=5)
        
        ModernButton(c, text="REGISTRAR", command=self.save).pack(fill='x', pady=(10,8))
        ModernButton(c, text="REGRESAR", type='secondary', command=self.destroy).pack(fill='x', pady=(0,10))

    def save(self):
        # Lógica resumida
        d = {k: v.get() for k, v in self.entries.items()}
        # Crear ID simple
        nid = len(self.controller.data['customers']) + 10
        new_c = Customer(nid, d['first_name'], "", d['last_name'], "", d['phone'], d['email'], d['state'], d['curp'], self.pw.get())
        self.controller.add_new_customer(new_c)
        messagebox.showinfo("OK", "Cliente registrado")
        self.destroy()

class RegisterEmployeeWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Registro Empleado")
        center_window(self, 500, 650)
        self.configure(bg=COLOR_BG)

        # Contenedor principal estilo Tarjeta (mismo estilo que RegisterCustomerWindow)
        c = ttk.Frame(self, style='Card.TFrame', padding=20)
        c.pack(fill='both', expand=True, padx=20, pady=20)
        ttk.Label(c, text="Nuevo Empleado", style='Title.TLabel').pack()

        f = ttk.Frame(c, style='Card.TFrame')
        f.pack(pady=10)

        # Campos del formulario (mismos márgenes/estilo que cliente)
        self.entries = {}
        fields = ["first_name", "middle_name", "last_name", "second_last_name", "phone", "email", "status", "curp"]
        for i, field in enumerate(fields):
            ttk.Label(f, text=field.replace('_', ' ').capitalize(), style='Card.TLabel').grid(row=i, column=0, sticky='w')
            e = ttk.Entry(f)
            e.grid(row=i, column=1, pady=5)
            self.entries[field] = e

        # Role selector
        ttk.Label(f, text="Role", style='Card.TLabel').grid(row=len(fields), column=0, sticky='w')
        self.role_var = tk.StringVar(value='Recepcionista')
        role_cb = ttk.Combobox(f, textvariable=self.role_var, values=["Recepcionista", "Botones", "Servicio"], state='readonly')
        role_cb.grid(row=len(fields), column=1, pady=5)

        # Password
        ttk.Label(f, text="Password", style='Card.TLabel').grid(row=len(fields)+1, column=0, sticky='w')
        self.pw = ttk.Entry(f, show='*'); self.pw.grid(row=len(fields)+1, column=1, pady=5)
        ttk.Label(f, text="Confirmar Password", style='Card.TLabel').grid(row=len(fields)+2, column=0, sticky='w')
        self.pw_confirm = ttk.Entry(f, show='*'); self.pw_confirm.grid(row=len(fields)+2, column=1, pady=5)

        # Botones: Registrar y Regresar (igual estilo que otros formularios)
        ModernButton(c, text="REGISTRAR EMPLEADO", command=self.process_registration).pack(fill='x', pady=(10,8))
        ModernButton(c, text="REGRESAR", type="secondary", command=self.go_back).pack(fill='x', pady=(0,10))

    def process_registration(self):
        # Recolectar datos
        data = {k: v.get().strip() for k, v in self.entries.items()}
        password = self.pw.get().strip()
        confirm = self.pw_confirm.get().strip()

        # Validaciones simples
        required = ['first_name', 'last_name', 'phone', 'email', 'status', 'curp']
        if not all(data.get(k) for k in required):
            messagebox.showwarning("Datos Incompletos", "Por favor complete los campos obligatorios.")
            return
        if password == "" or password != confirm:
            messagebox.showerror("Contraseña", "Las contraseñas están vacías o no coinciden.")
            return

        # Calcular nuevo ID
        try:
            existing_ids = [int(k) for k in self.controller.data['employees'].keys()]
            new_id = max(existing_ids) + 1 if existing_ids else 1
        except Exception:
            new_id = 1

        role = self.role_var.get()
        # Crear la instancia según role
        if role == 'Recepcionista':
            new_emp = Receptionist(new_id, data['first_name'], data.get('middle_name',''), data['last_name'], data.get('second_last_name',''), data['phone'], data['email'], data['status'], data['curp'], password)
        elif role == 'Botones':
            new_emp = Bellboy(new_id, data['first_name'], data.get('middle_name',''), data['last_name'], data.get('second_last_name',''), data['phone'], data['email'], data['status'], data['curp'], password)
        else:
            new_emp = Employee(new_id, data['first_name'], data.get('middle_name',''), data['last_name'], data.get('second_last_name',''), data['phone'], data['email'], data['status'], data['curp'], password)

        self.controller.add_new_employee(new_emp)
        messagebox.showinfo("Registro Exitoso", f"Empleado {data['first_name']} {data['last_name']} registrado.")
        self.destroy()

    def go_back(self):
        try:
            self.controller.show_frame("WelcomeScreen")
        except Exception:
            pass
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    # Intento de mejora de renderizado de fuentes en Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    app = HotelGUI(root)
    root.mainloop()