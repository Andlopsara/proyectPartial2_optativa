class Room:
    def __init__(self, id, room_number, type, status="Available", cost=0.0, description=""):
        self.__id = id
        self.__room_number = room_number
        self.__type = type
        self.__status = status
        self.__cost = cost
        self.__description = description

    # -------- Getters and Setters --------
    def getId(self): return self.__id
    def setId(self, id): self.__id = id

    def getRoomNumber(self): return self.__room_number
    def setRoomNumber(self, room_number): self.__room_number = room_number

    def getType(self): return self.__type
    def setType(self, type): self.__type = type

    def getStatus(self): return self.__status
    def setStatus(self, status): self.__status = status

    def getCost(self): return self.__cost
    def setCost(self, cost): self.__cost = cost

    def getDescription(self): return self.__description
    def setDescription(self, description): self.__description = description

    # -------- Métodos --------
    def assignCustomer(self, customer):
        if self.__status == "Available":
            self.__status = "Not available"
            print(f"Room {self.__id} assigned to {customer.getName()}.")
        else:
            print(f"Room {self.__id} is not available for {customer.getName()}.")

    def releaseRoom(self):
        self.__status = "Available"
        print(f"Room {self.__id} released.")

    def showInfo(self):
        print(f"Room {self.__id} - Type: {self.__type} - Status: {self.__status} - Cost: ${self.__cost} - Description: {self.__description}")
