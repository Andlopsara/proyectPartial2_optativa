class Reservation:
    def __init__(self, id, checkIn, checkOut, customer, room, payment=None):
        self.__id = id
        self.__checkIn = checkIn
        self.__checkOut = checkOut
        self.__customer = customer
        self.__room = room
        self.__payment = payment
        self.__services = []

    # -------- Getters and Setters --------
    def getId(self): return self.__id
    def setId(self, id): self.__id = id

    def getCheckIn(self): return self.__checkIn
    def setCheckIn(self, checkIn): self.__checkIn = checkIn

    def getCheckOut(self): return self.__checkOut
    def setCheckOut(self, checkOut): self.__checkOut = checkOut

    def getCustomer(self): return self.__customer
    def setCustomer(self, customer): self.__customer = customer

    def getRoom(self): return self.__room
    def setRoom(self, room): self.__room = room

    def getPayment(self): return self.__payment
    def setPayment(self, payment): self.__payment = payment

    def getServices(self): return self.__services

    # -------- Métodos --------
    def createReservation(self):
        """Crea la reserva si la habitación está disponible."""
        if self.__room.getStatus() == "Available":
            self.__room.assignCustomer(self.__customer)
            # Ahora llama al método makeReservation que ya existe en Customer
            self.__customer.makeReservation(self)
            print(f"Reservation #{self.__id} created successfully for {self.__customer.getName()}")
            return True
        else:
            print(f"Unable to create reservation. Room {self.__room.getId()} not available.")
            return False

    def cancelReservation(self):
        """Cancela la reserva y libera la habitación."""
        self.__room.releaseRoom()
        print(f"Reservation #{self.__id} cancelled. Room {self.__room.getId()} released.")

    def modifyReservation(self, newCheckIn=None, newCheckOut=None):
        """Modifica las fechas de entrada y/o salida de la reserva."""
        if newCheckIn:
            self.__checkIn = newCheckIn
            print(f"Reservation #{self.__id} check-in date updated to {newCheckIn}.")
        if newCheckOut:
            self.__checkOut = newCheckOut
            print(f"Reservation #{self.__id} check-out date updated to {newCheckOut}.")

    def addService(self, service):
        """Añade un servicio a la reserva."""
        self.__services.append(service)
        print(f"Service '{service.getType()}' added to reservation #{self.__id}.")
        
    def showInfo(self):
        """AÑADIDO: Muestra la información esencial de la reserva."""
        customer_name = self.__customer.getName() if hasattr(self.__customer, 'getName') else 'Unknown Customer'
        room_id = self.__room.getId() if hasattr(self.__room, 'getId') else 'Unknown Room'
        info = (
            f"--- Información de la Reserva #{self.__id} ---\n"
            f"  Cliente: {customer_name}\n"
            f"  Habitación: {room_id} ({self.__room.getType()})\n"
            f"  Llegada: {self.__checkIn} | Salida: {self.__checkOut}\n"
            f"  Servicios Adicionales: {len(self.__services)}"
        )
        print(info)
        return info