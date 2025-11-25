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

    # -------- Métodos --------
    def registerCustomer(self):
        print(f"Customer {self.__name} has been registered.")

    def checkReservation(self):
        if not self.__reservations:
            print(f"Customer {self.__name} has no reservations.")
        else:
            print(f"Customer {self.__name} has {len(self.__reservations)} reservation(s).")

    def makeReservation(self, reservation):
        self.__reservations.append(reservation)
        print(f"Reservation made by {self.__name} for room {reservation.getRoom().getId()}.")
