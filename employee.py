class Employee:
    def __init__(self, id, firstName, secondName, lastName, secondLastName, phone, email, status, curp, password=""):
        self.__id = id
        self.__firstName = firstName
        self.__secondName = secondName
        self.__lastName = lastName
        self.__secondLastName = secondLastName
        self.__phone = phone
        self.__email = email
        self.__status = status
        self.__curp = curp
        self.__password = password

    # -------- Getters and Setters --------
    def getId(self): return self.__id
    def setId(self, id): self.__id = id

    def getFirstName(self): return self.__firstName
    def setFirstName(self, firstName): self.__firstName = firstName

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

    def getPassword(self): return getattr(self, '_Employee__password', '')
    def setPassword(self, password): self.__password = password

    def getStatus(self): return self.__status
    def setStatus(self, status): self.__status = status

    def getCurp(self): return self.__curp
    def setCurp(self, curp): self.__curp = curp

    # -------- Métodos --------
    def createReservation(self, reservation):
        reservation.createReservation()
        print(f"Employee {self.__firstName} created a reservation for room {reservation.getRoom().getId()}.")

    def cancelReservation(self, reservation):
        reservation.cancelReservation()
        print(f"Employee {self.__firstName} cancelled reservation for room {reservation.getRoom().getId()}.")

    def modifyReservation(self, reservation, newCheckIn=None, newCheckOut=None):
        reservation.modifyReservation(newCheckIn, newCheckOut)
        print(f"Employee {self.__firstName} modified reservation for room {reservation.getRoom().getId()}.")

    def registerService(self, service):
        service.addService()
        print(f"Employee {self.__firstName} registered service {service.getType()}.")

