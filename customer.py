from typing import List

class Customer:
    def __init__(self, id, name, secondName, lastName, secondLastName, phone, email, state, curp):
        self.__id = id
        self.__name = name
        self.__secondName = secondName
        self.__lastName = lastName
        self.__secondLastName = secondLastName
        self.__phone = phone
        self.__email = email
        self.__state = state
        self.__curp = curp
        self.__reservations: List = []
        self.__service_reservations: List = []

    # -------- Getters and Setters --------
    def getId(self): return self.__id
    def setId(self, id): self.__id = id

    def getName(self): return self.__name
    def setName(self, name): self.__name = name

    def getSecondName(self): return self.__secondName
    def setSecondName(self, secondName): self.__secondName = secondName

    def getLastName(self): return self.__lastName
    def setLastName(self, lastName): self.__lastName = lastName

    def getSecondLastName(self): return self.__secondLastName
    def setSecondLastName(self, secondLastName): self.__secondLastName = secondLastName

    def getPhone(self): return self.__phone
    def setPhone(self, phone): self.__phone = phone

    def getEmail(self): return self.__email
    def setEmail(self, email): self.__email = email

    def getState(self): return self.__state
    def setState(self, state): self.__state = state

    def getCurp(self): return self.__curp
    def setCurp(self, curp): self.__curp = curp

    def getReservations(self): return self.__reservations

    def getServiceReservations(self):
        """Devuelve la lista de reservas de servicios del cliente."""
        return self.__service_reservations

    # -------- Métodos --------
    def registerCustomer(self):
        """Registra al cliente (muestra un mensaje en consola)."""
        print(f"Customer {self.__name} has been registered.")

    def makeReservation(self, reservation):
        """AÑADIDO: Almacena el objeto de la reserva en el historial del cliente."""
        self.__reservations.append(reservation)
        print(f"Reservation #{reservation.getId()} added to customer {self.__name}'s record.")
        
    def checkReservation(self):
        """Verifica y muestra las reservas del cliente. Esto es la 'vista' de la reserva."""
        if not self.__reservations:
            print(f"Customer {self.__name} has no reservations.")
        else:
            print(f"Customer {self.__name} has {len(self.__reservations)} reservation(s).")
            for res in self.__reservations:
                # Llama al método showInfo() de la clase Reservation
                res.showInfo() 

    def cancelReservation(self, reservation_id):
        """Elimina la reserva del registro del cliente por ID."""
        initial_count = len(self.__reservations)
        self.__reservations = [res for res in self.__reservations if res.getId() != reservation_id]
        if len(self.__reservations) < initial_count:
            print(f"Reservation #{reservation_id} removed from customer {self.__name}'s record.")
            return True
        return False

    # -------- Reservas de Servicio --------
    def makeServiceReservation(self, service_reservation):
        """Agrega una reserva de servicio al historial del cliente."""
        self.__service_reservations.append(service_reservation)
        print(f"Service Reservation #{service_reservation.getId()} added to customer {self.__name}'s record.")

    def cancelServiceReservation(self, reservation_id):
        """Elimina una reserva de servicio por ID."""
        initial_count = len(self.__service_reservations)
        self.__service_reservations = [res for res in self.__service_reservations if res.getId() != reservation_id]
        if len(self.__service_reservations) < initial_count:
            print(f"Service Reservation #{reservation_id} removed from customer {self.__name}'s record.")
            return True
        return False