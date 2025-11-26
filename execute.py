import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
import re 
import uuid 

from customer import Customer
from service import Service 
from reservationService import ServiceReservation 
from reservation import Reservation 
from room import Room
from employee import Employee
from receptionist import Receptionist
from bellboy import Bellboy
from payment import Payment

from dao.employee_dao import EmployeeDAO
from dao.ServiceDAO import ServiceDAO
from dao.customer_dao import CustomerDAO
from dao.room_dao import RoomDAO
from dao.payment_dao import PaymentDAO
from dao.reservation_dao import ReservationDAO

COLOR_PRIMARY = '#1A237E'
COLOR_SECONDARY = '#283593'
COLOR_ACCENT = '#D4AF37'
COLOR_BG = '#F5F6FA'
COLOR_WHITE = '#FFFFFF'
COLOR_TEXT = '#2C3E50'
COLOR_TEXT_LIGHT = '#7F8C8D'
COLOR_DANGER = '#C0392B'

FONT_HEADER = ('Segoe UI', 20, 'bold')
FONT_SUBHEADER = ('Segoe UI', 14, 'bold')
FONT_BODY = ('Segoe UI', 10)
FONT_BODY_BOLD = ('Segoe UI', 10, 'bold')
FONT_BUTTON = ('Segoe UI', 10, 'bold')

#inicializar datos desde la base de datos
def init_data_from_db():
    print("--- Cargando datos iniciales desde la Base de Datos ---")
    customer_dao = CustomerDAO()
    employee_dao = EmployeeDAO()
    service_dao = ServiceDAO()
    room_dao = RoomDAO()
    reservation_dao = ReservationDAO()

    all_customers = customer_dao.get_all()
    all_employees = employee_dao.get_all()
    all_services = service_dao.get_all()
    all_rooms = room_dao.get_all()
    all_reservations = reservation_dao.get_all()

    service_reservations = {}

    return {
        'customers': {c.getEmail(): c for c in all_customers}, 
        'employees': {e.getEmail(): e for e in all_employees}, 
        'rooms': {r.getId(): r for r in all_rooms},
        'reservations': {r.getId(): r for r in all_reservations},
        'service_reservations': service_reservations,
        'services': {s.getId(): s for s in all_services}
    }

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))
    window.geometry(f"{width}x{height}+{x}+{y}")

class ModernButton(tk.Button):
    def __init__(self, parent, text, command=None, **kwargs):
        button_type = kwargs.pop('type', kwargs.pop('button_type', 'primary'))
        
        background = COLOR_PRIMARY if button_type == "primary" else (COLOR_ACCENT if button_type == "accent" else COLOR_WHITE)
        foreground = COLOR_WHITE if button_type in ["primary", "accent"] else COLOR_PRIMARY
        
        super().__init__(parent, text=text, command=command, 
                         bg=background, fg=foreground, 
                         font=FONT_BUTTON, relief="flat", 
                         activebackground=COLOR_SECONDARY, activeforeground=COLOR_WHITE,
                         bd=0, padx=20, pady=10, cursor="hand2", **kwargs)

class HotelGUI:
    def __init__(self, master):
        self.master = master
        master.title("Le Villa Hotel Management")
        master.configure(bg=COLOR_BG)
        center_window(master, 900, 600)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TFrame', background=COLOR_BG)
        self.style.configure('Card.TFrame', background=COLOR_WHITE, relief="groove", borderwidth=1)
        
        self.style.configure('TLabel', background=COLOR_BG, foreground=COLOR_TEXT, font=FONT_BODY)
        self.style.configure('Card.TLabel', background=COLOR_WHITE, foreground=COLOR_TEXT, font=FONT_BODY)
        self.style.configure('Header.TLabel', font=FONT_HEADER, foreground=COLOR_PRIMARY, background=COLOR_BG)
        self.style.configure('Title.TLabel', font=FONT_SUBHEADER, foreground=COLOR_PRIMARY, background=COLOR_WHITE)
        
        self.style.configure('TEntry', padding=5, relief="flat", borderwidth=1)
        self.style.map('TEntry', bordercolor=[('focus', COLOR_PRIMARY)])

        self.container = ttk.Frame(master)
        self.container.pack(fill="both", expand=True)
        
        self.data = init_data_from_db()
        
        self.next_reservation_id = max(self.data['reservations'].keys()) + 1 if self.data['reservations'] else 1
        self.next_service_reservation_id = max(self.data['service_reservations'].keys()) + 1 if self.data['service_reservations'] else 1
        self.next_payment_id = 1
        self.data['payments'] = {}
        
        self.frames = {}

        self.employee_dao = EmployeeDAO()
        self.service_dao = ServiceDAO()
        self.customer_dao = CustomerDAO()
        self.room_dao = RoomDAO()
        self.payment_dao = PaymentDAO()
        self.reservation_dao = ReservationDAO()

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

class CreateServiceReservationWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Solicitar Nuevo Servicio")
        center_window(self, 500, 600)
        self.configure(bg=COLOR_BG)

        card = ttk.Frame(self, style='Card.TFrame', padding=20)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(card, text="🛎️ Solicitar Servicio", style='Title.TLabel').pack(pady=(0, 20))
        
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

        ttk.Label(form_frame, text="Habitacion (Opcional)", style='Card.TLabel', font=FONT_BODY_BOLD).pack(anchor='w')
        self.room_number_entry = ttk.Entry(form_frame, width=40)
        self.room_number_entry.pack(fill='x', pady=(5, 15))
        self.room_number_entry.insert(0, "101")

        ttk.Label(form_frame, text="Servicio", style='Card.TLabel', font=FONT_BODY_BOLD).pack(anchor='w')
        self.services = self.controller.data.get('services', {})
        service_options = [f"{s.getId()}: {s.getType()} (${s.getCost():.2f})" for s in self.services.values()]
        
        self.service_var = tk.StringVar(form_frame)
        self.service_combo = ttk.Combobox(form_frame, textvariable=self.service_var, values=service_options, state="readonly")
        self.service_combo.pack(fill='x', pady=(5, 15))
        if service_options: self.service_combo.set(service_options[0])

        ttk.Label(form_frame, text="Fecha/Hora", style='Card.TLabel', font=FONT_BODY_BOLD).pack(anchor='w')
        self.datetime_entry = ttk.Entry(form_frame, width=40)
        self.datetime_entry.pack(fill='x', pady=(5, 20))
        self.datetime_entry.insert(0, str(date.today()) + " 10:00")
        
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
            messagebox.showerror("Error", "Formato de fecha invalido.")
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
        
        ttk.Label(card, text="Detalles del Pago", style='Title.TLabel').pack(pady=(0, 20))
        
        info_frame = ttk.Frame(card, style='Card.TFrame')
        info_frame.pack(fill='x', pady=10)
        
        ttk.Label(info_frame, text=f"Servicio: {reservation._ServiceReservation__service.getType()}", style='Card.TLabel').pack(anchor='w')
        ttk.Label(info_frame, text=f"Cliente: {customer.getName()}", style='Card.TLabel').pack(anchor='w')
        
        ttk.Separator(card, orient='horizontal').pack(fill='x', pady=15)
        
        ttk.Label(card, text="TOTAL A PAGAR", style='Card.TLabel', font=('Segoe UI', 10)).pack()
        ttk.Label(card, text=f"${service_cost:.2f}", style='Card.TLabel', font=('Segoe UI', 24, 'bold'), foreground=COLOR_PRIMARY).pack(pady=5)
        
        ttk.Label(card, text="Metodo de Pago:", style='Card.TLabel', font=FONT_BODY_BOLD).pack(anchor='w', pady=(15, 5))
        self.payment_method_var = tk.StringVar(value="Tarjeta de Credito")
        
        s = ttk.Style()
        s.configure('TRadiobutton', background=COLOR_WHITE, font=FONT_BODY)
        
        ttk.Radiobutton(card, text="Tarjeta de Credito", variable=self.payment_method_var, value="Tarjeta de Credito").pack(anchor='w')
        ttk.Radiobutton(card, text="Efectivo", variable=self.payment_method_var, value="Efectivo").pack(anchor='w')
        
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
        new_payment_id = self.controller.payment_dao.create(payment)
        if new_payment_id:
            messagebox.showinfo("Pago Exitoso", f"El pago #{new_payment_id} ha sido procesado y guardado.")
        else:
            messagebox.showerror("Error de Base de Datos", "El pago fue procesado pero no se pudo guardar en la base de datos.")
        self.destroy()

class WelcomeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        header = tk.Frame(self, bg=COLOR_PRIMARY, height=150)
        header.pack(fill='x')
        
        title = tk.Label(header, text="LE VILLA", font=('Times New Roman', 40, 'bold'), bg=COLOR_PRIMARY, fg=COLOR_ACCENT)
        title.place(relx=0.5, rely=0.5, anchor='center')
        
        subtitle = tk.Label(header, text="HOTEL & SPA", font=('Segoe UI', 12, 'bold'), bg=COLOR_PRIMARY, fg=COLOR_WHITE)
        subtitle.place(relx=0.5, rely=0.75, anchor='center')
        
        content = tk.Frame(self, bg=COLOR_BG)
        content.pack(fill='both', expand=True, padx=50, pady=30)
        
        tk.Label(content, text="Seleccione su perfil para acceder", font=FONT_SUBHEADER, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=20)
        
        btn_container = tk.Frame(content, bg=COLOR_BG)
        btn_container.pack()
        
        ModernButton(btn_container, text="ACCESO HUESPED", type="primary", 
                     command=lambda: controller.show_frame("LoginFormScreen", login_type="Customer")).grid(row=0, column=0, padx=10, pady=10)
        
        ModernButton(btn_container, text="ACCESO EMPLEADO", type="primary",
                     command=lambda: controller.show_frame("LoginFormScreen", login_type="Employee")).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Frame(content, height=1, bg="#DDDDDD", width=300).pack(pady=20)
        
        reg_frame = tk.Frame(content, bg=COLOR_BG)
        reg_frame.pack()
        
        tk.Button(reg_frame, text="Crear cuenta Huesped", font=('Segoe UI', 9, 'underline'), 
                  bg=COLOR_BG, fg=COLOR_TEXT, bd=0, cursor="hand2",
                  command=lambda: RegisterCustomerWindow(controller.master, controller)).pack(side="left", padx=20)
                  
        tk.Button(reg_frame, text="Crear cuenta Empleado", font=('Segoe UI', 9, 'underline'),
                  bg=COLOR_BG, fg=COLOR_TEXT, bd=0, cursor="hand2",
                  command=lambda: RegisterEmployeeWindow(controller.master, controller)).pack(side="left", padx=20)


class LoginFormScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        right_panel = tk.Frame(self, bg=COLOR_BG)
        right_panel.pack(fill='both', expand=True, padx=50, pady=30)

        center_frame = tk.Frame(right_panel, bg=COLOR_BG)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        self.title_label = tk.Label(center_frame, text="INICIAR SESION", font=FONT_HEADER, bg=COLOR_BG, fg=COLOR_PRIMARY)
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
            self.title_label.config(text="ACCESO HUESPED")
            self.email_entry.delete(0, tk.END)
        else: 
            self.title_label.config(text="ACCESO EMPLEADO")
            self.email_entry.delete(0, tk.END)

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
            user_obj = self.controller.data['employees'].get(email)
            if user_obj and user_obj.getPassword() == password:
                self.controller.show_frame("MainMenuScreen", user_type="Employee", user_obj=user_obj)
            else:
                messagebox.showerror("Error", "Credenciales invalidas.")


class LoginSuccessScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
class MainMenuScreen(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        top_bar = tk.Frame(self, bg=COLOR_WHITE, height=60)
        top_bar.pack(side='top', fill='x')
        top_bar.pack_propagate(False)
        
        tk.Label(top_bar, text="LE VILLA -HOTEL & SPA- ", font=('Times New Roman', 14, 'bold'), bg=COLOR_WHITE, fg=COLOR_PRIMARY).pack(side='left', padx=20)
        self.user_label = tk.Label(top_bar, text="", font=FONT_BODY, bg=COLOR_WHITE, fg=COLOR_TEXT)
        self.user_label.pack(side='right', padx=20)
        
        self.main_area = tk.Frame(self, bg=COLOR_BG)
        self.main_area.pack(fill='both', expand=True, padx=40, pady=40)
        
        self.grid_buttons_frame = tk.Frame(self.main_area, bg=COLOR_BG)
        self.grid_buttons_frame.pack(anchor='center')

    def create_dashboard_card(self, parent, icon, title, command, row, col):
        frame = tk.Frame(parent, bg=COLOR_WHITE, width=200, height=150)
        frame.grid(row=row, column=col, padx=15, pady=15)
        frame.pack_propagate(False) 
        
        
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

        for widget in self.grid_buttons_frame.winfo_children():
            widget.destroy()

        self.create_dashboard_card(self.grid_buttons_frame, "📅", "Reservar Habitacion", self.open_create_reservation, 0, 0)
        self.create_dashboard_card(self.grid_buttons_frame, "🛎️", "Solicitar Servicio", self.open_create_service_reservation, 0, 1)
        self.create_dashboard_card(self.grid_buttons_frame, "👁️", "Ver mis Reservas", self.view_room_reservation, 0, 2)
        
        self.create_dashboard_card(self.grid_buttons_frame, "🍽️", "Ver Servicios Activos", self.view_service_reservation, 1, 0)
        self.create_dashboard_card(self.grid_buttons_frame, "ℹ️", "Info de las habitaciones", self.view_room_info, 1, 1)

    def open_create_reservation(self): CreateReservationWindow(self.controller.master, self.controller)
    def open_create_service_reservation(self): CreateServiceReservationWindow(self.controller.master, self.controller)


    def view_room_reservation(self):
        ViewReservationsWindow(self.controller.master, self.controller)

    def view_service_reservation(self):
        ViewServicesWindow(self.controller.master, self.controller)

    def view_room_info(self):
        RoomInfoWindow(self.controller.master, self.controller)


class CreateReservationWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller

        self.title("Reservar Habitacion") # <-- El código huérfano empieza aquí
        center_window(self, 600, 700)
        self.configure(bg=COLOR_BG)
        
        container = ttk.Frame(self, style='Card.TFrame', padding=20)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(container, text="Nueva Reserva", style='Title.TLabel').pack(pady=(0, 20))

        f = ttk.Frame(container, style='Card.TFrame')
        f.pack(fill='both', expand=True)

        self.create_field(f, "Email Cliente:", 0)
        self.email_entry = ttk.Entry(f, width=30); self.email_entry.grid(row=0, column=1, pady=10)
        if controller.frames['MainMenuScreen'].user_type == 'Customer':
            self.email_entry.insert(0, controller.frames['MainMenuScreen'].user_obj.getEmail())

        self.create_field(f, "Tipo Habitacion:", 1)
        self.room_type_var = tk.StringVar(value="Suite")
        self.cb_type = ttk.Combobox(f, textvariable=self.room_type_var, values=["Suite", "Doble", "Individual"], state="readonly")
        self.cb_type.grid(row=1, column=1, pady=10)
        
        self.create_field(f, "Registro entrada (AAAA-MM-DD):", 2)
        self.in_entry = ttk.Entry(f); self.in_entry.insert(0, str(date.today())); self.in_entry.grid(row=2, column=1, pady=10)

        self.create_field(f, "Registro salida (AAAA-MM-DD):", 3)
        self.out_entry = ttk.Entry(f); self.out_entry.insert(0, "2025-12-31"); self.out_entry.grid(row=3, column=1, pady=10)

        self.create_field(f, "Habitacion Disponible:", 4)
        all_rooms = self.controller.data.get('rooms', {}).values()
        available_rooms = [r for r in all_rooms if r.getStatus().lower() == 'available']
        room_options = [f"{r.getId()}: {r.getType()} (${r.getCost():.2f})" for r in available_rooms]
        self.room_var = tk.StringVar()
        self.room_cb = ttk.Combobox(f, textvariable=self.room_var, values=room_options, state='readonly')
        self.room_cb.grid(row=4, column=1, pady=10)
        if room_options: self.room_cb.set(room_options[0])
        
        ttk.Label(f, text="Servicio Adicional:", style='Card.TLabel', font=FONT_BODY_BOLD).grid(row=5, column=0, sticky='w', padx=10)
        services = self.controller.data.get('services', {})
        service_options = ["Ninguno"] + [f"{s.getId()}: {s.getType()} (${s.getCost():.2f})" for s in services.values()]
        self.service_var = tk.StringVar(value="Ninguno")
        self.service_cb = ttk.Combobox(f, textvariable=self.service_var, values=service_options, state='readonly')
        self.service_cb.grid(row=5, column=1, pady=10)

        ModernButton(container, text="CONFIRMAR RESERVA", type="primary", command=self.process).pack(fill='x', pady=(10,8))
        ModernButton(container, text="REGRESAR", type="secondary", command=self.destroy).pack(fill='x', pady=(0,10))

    def create_field(self, parent, text, row):
        ttk.Label(parent, text=text, style='Card.TLabel', font=FONT_BODY_BOLD).grid(row=row, column=0, sticky='w', padx=10)

    def process(self):
        room_info = self.room_var.get()
        try:
            rid = int(room_info.split(':')[0])
        except Exception:
            messagebox.showerror("Error", "Debe seleccionar una habitacion valida.")
            return

        room = self.controller.data.get('rooms', {}).get(rid)
        cust = self.controller.data['customers'].get(self.email_entry.get())

        if not room or not cust:
            messagebox.showerror("Error", "Datos invalidos: cliente o habitacion no encontrados.")
            return

        from datetime import datetime
        try:
            check_in = datetime.strptime(self.in_entry.get().strip(), "%Y-%m-%d").date()
            check_out = datetime.strptime(self.out_entry.get().strip(), "%Y-%m-%d").date()
        except Exception:
            messagebox.showerror("Fecha invalida", "Formato de fecha invalido. Use AAAA-MM-DD.")
            return

        if check_out <= check_in:
            messagebox.showerror("Fechas invalidas", "La fecha de salida debe ser posterior a la fecha de entrada.")
            return

        try:
            res = Reservation(self.controller.next_reservation_id, self.in_entry.get().strip(), self.out_entry.get().strip(), cust, room)
            if not res.createReservation():
                messagebox.showerror("Error", "Habitacion no disponible.")
                return

            num_nights = (check_out - check_in).days
            room_subtotal = room.getCost() * num_nights

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

            new_res_id = self.controller.reservation_dao.create(res, total_cost)
            if not new_res_id:
                messagebox.showerror("Error de Base de Datos", "No se pudo registrar la reserva. Intente de nuevo.")
                return
            
            self.controller.data['reservations'][new_res_id] = res

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
        
        ttk.Label(card, text="Pago de Habitacion", style='Title.TLabel').pack(pady=10)

        if self.room_subtotal is None:
            try:
                from datetime import datetime
                check_in = datetime.strptime(self.reservation.getCheckIn(), "%Y-%m-%d").date()
                check_out = datetime.strptime(self.reservation.getCheckOut(), "%Y-%m-%d").date()
                nights = (check_out - check_in).days
                self.room_subtotal = self.reservation.getRoom().getCost() * max(1, nights)
            except Exception:
                self.room_subtotal = self.total_cost

        ttk.Label(card, text=f"Habitacion: ${self.room_subtotal:.2f}", style='Card.TLabel').pack(pady=(8,2))
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

        btn_frame = ttk.Frame(card)
        btn_frame.pack(fill='x', pady=(12,0))
        ModernButton(btn_frame, text="PAGAR", command=self.pay).pack(side='left', fill='x', expand=True, padx=(0,6))
        ModernButton(btn_frame, text="REGRESAR", type='secondary', command=self.destroy).pack(side='right', fill='x', expand=True, padx=(6,0))
        
    def pay(self):
        p = Payment(self.controller.next_payment_id, self.total_cost, self.method.get(), self.reservation)
        p.processPayment()
        new_payment_id = self.controller.payment_dao.create(p)
        if new_payment_id:
            messagebox.showinfo("Exito", f"Pago #{new_payment_id} completado y guardado.")
            self.controller.reservation_dao.link_payment(self.reservation.getId(), new_payment_id)
        else:
            messagebox.showerror("Error de Base de Datos", "El pago fue procesado pero no se pudo guardar en la base de datos.")
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
        
        tree_frame = ttk.Frame(card)
        tree_frame.pack(fill='both', expand=True, pady=5)
        
        columns = ('id', 'customer', 'room', 'check_in', 'check_out', 'cost')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('customer', text='Cliente')
        self.tree.heading('room', text='Habitación')
        self.tree.heading('check_in', text='Check-In')
        self.tree.heading('check_out', text='Check-Out')
        self.tree.heading('cost', text='Costo Total')
        
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('customer', width=150)
        self.tree.column('room', width=80, anchor='center')
        self.tree.column('check_in', width=100, anchor='center')
        self.tree.column('check_out', width=100, anchor='center')
        self.tree.column('cost', width=80, anchor='e')

        self.tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.load_reservations()

        btn_frame = ttk.Frame(card, style='Card.TFrame')
        btn_frame.pack(fill='x', pady=(10, 0))

        if self.controller.frames['MainMenuScreen'].user_type == 'Employee':
            ModernButton(btn_frame, text="Eliminar Reserva Seleccionada", type="secondary", command=self.delete_selected_reservation).pack(side='left')

        ModernButton(btn_frame, text="Cerrar", command=self.destroy).pack(side='right')

    def load_reservations(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        reservations = self.controller.data.get('reservations', {}).values()
        for res in sorted(reservations, key=lambda r: r.getId()):
            customer_name = res.getCustomer().getName()
            room_number = res.getRoom().getRoomNumber()
            total_cost = f"${res.getRoom().getCost():.2f}" # Simplificado, el costo real está en la tabla RESERVATIONS
            self.tree.insert('', 'end', values=(res.getId(), customer_name, room_number, res.getCheckIn(), res.getCheckOut(), total_cost))

    def delete_selected_reservation(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Sin SelecciOn", "Por favor, seleccione una reserva de la lista para eliminar.")
            return

        values = self.tree.item(selected_item, 'values')
        reservation_id = int(values[0])
        customer_name = values[1]

        if messagebox.askyesno("Confirmar Eliminacion", f"¿Esta seguro de que desea eliminar la reserva #{reservation_id} de {customer_name}?"):
            if self.controller.reservation_dao.delete(reservation_id):
                messagebox.showinfo("Exito", f"La reserva #{reservation_id} ha sido eliminada.")
                self.tree.delete(selected_item)
                del self.controller.data['reservations'][reservation_id]
            else:
                messagebox.showerror("Error de Base de Datos", "No se pudo eliminar la reserva.")


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
        self.title("Informacion de Habitaciones")
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
            txt.insert('end', 'No hay informacion de habitaciones.')
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
        
        c = ttk.Frame(self, style='Card.TFrame', padding=20); c.pack(fill='both', expand=True, padx=20, pady=20)
        ttk.Label(c, text="Nuevo Huesped", style='Title.TLabel').pack()
        
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
        data = {k: v.get().strip() for k, v in self.entries.items()}
        password = self.pw.get().strip()

        if not all([data.get('first_name'), data.get('last_name'), data.get('email'), password]):
            messagebox.showwarning("Datos Incompletos", "Nombre, apellido, email y contraseña son obligatorios.")
            return

        new_customer = Customer(0, data['first_name'], "", data['last_name'], "", data['phone'], data['email'], data['state'], data['curp'], password)
        
        new_id = self.controller.customer_dao.create(new_customer)
        if new_id:
            messagebox.showinfo("Registro Exitoso", f"Cliente {new_customer.getName()} registrado con ID: {new_id}.")
            self.controller.data['customers'][new_customer.getEmail()] = new_customer
            self.destroy()
        else:
            messagebox.showerror("Error de Base de Datos", "No se pudo registrar al cliente. Revise la consola.")

class RegisterEmployeeWindow(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.title("Registro Empleado")
        center_window(self, 500, 650)
        self.configure(bg=COLOR_BG)

        c = ttk.Frame(self, style='Card.TFrame', padding=20)
        c.pack(fill='both', expand=True, padx=20, pady=20)
        ttk.Label(c, text="Nuevo Empleado", style='Title.TLabel').pack()

        f = ttk.Frame(c, style='Card.TFrame')
        f.pack(pady=10)

        self.entries = {}
        fields = ["first_name", "middle_name", "last_name", "second_last_name", "phone", "email", "status", "curp"]
        for i, field in enumerate(fields):
            ttk.Label(f, text=field.replace('_', ' ').capitalize(), style='Card.TLabel').grid(row=i, column=0, sticky='w')
            e = ttk.Entry(f)
            e.grid(row=i, column=1, pady=5)
            self.entries[field] = e

        ttk.Label(f, text="Role", style='Card.TLabel').grid(row=len(fields), column=0, sticky='w')
        self.role_var = tk.StringVar(value='Recepcionista')
        role_cb = ttk.Combobox(f, textvariable=self.role_var, values=["Recepcionista", "Botones", "Servicio"], state='readonly')
        role_cb.grid(row=len(fields), column=1, pady=5)

        ttk.Label(f, text="Password", style='Card.TLabel').grid(row=len(fields)+1, column=0, sticky='w')
        self.pw = ttk.Entry(f, show='*'); self.pw.grid(row=len(fields)+1, column=1, pady=5)
        ttk.Label(f, text="Confirmar Password", style='Card.TLabel').grid(row=len(fields)+2, column=0, sticky='w')
        self.pw_confirm = ttk.Entry(f, show='*'); self.pw_confirm.grid(row=len(fields)+2, column=1, pady=5)

        ModernButton(c, text="REGISTRAR EMPLEADO", command=self.process_registration).pack(fill='x', pady=(10,8))
        ModernButton(c, text="REGRESAR", type="secondary", command=self.go_back).pack(fill='x', pady=(0,10))

    def process_registration(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        password = self.pw.get().strip()
        confirm = self.pw_confirm.get().strip()

        required = ['first_name', 'last_name', 'phone', 'email', 'status', 'curp']
        if not all(data.get(k) for k in required):
            messagebox.showwarning("Datos Incompletos", "Por favor complete los campos obligatorios.")
            return
        if password == "" or password != confirm:
            messagebox.showerror("Contraseña", "Las contraseñas están vacias o no coinciden.")
            return

        try:
            existing_ids = [int(k) for k in self.controller.data['employees'].keys()]
            new_id = max(existing_ids) + 1 if existing_ids else 1
        except Exception:
            new_id = 1

        role = self.role_var.get()
        if role == 'Recepcionista':
            new_emp = Receptionist(new_id, data['first_name'], data.get('middle_name',''), data['last_name'], data.get('second_last_name',''), data['phone'], data['email'], data['status'], data['curp'], password)
        elif role == 'Botones':
            new_emp = Bellboy(new_id, data['first_name'], data.get('middle_name',''), data['last_name'], data.get('second_last_name',''), data['phone'], data['email'], data['status'], data['curp'], password)
        else:
            new_emp = Employee(new_id, data['first_name'], data.get('middle_name',''), data['last_name'], data.get('second_last_name',''), data['phone'], data['email'], data['status'], data['curp'], password)
        
        new_id_from_db = self.controller.employee_dao.create(new_emp)
        
        if new_id_from_db:
            messagebox.showinfo("Registro Exitoso", f"Empleado {new_emp.getFirstName()} registrado en la base de datos con ID: {new_id_from_db}.")
            self.controller.data['employees'][new_emp.getEmail()] = new_emp
            self.destroy()
        else:
            messagebox.showerror("Error de Base de Datos", "No se pudo registrar al empleado. Revise la consola para más detalles.")

    def go_back(self):
        try:
            self.controller.show_frame("WelcomeScreen")
        except Exception:
            pass
        self.destroy()


if __name__ == '__main__':
    raiz = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    aplicacion = HotelGUI(raiz)
    raiz.mainloop()