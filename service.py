class Service:
    def __init__(self, id, type, cost, description):
        self.__id = id
        self.__type = type
        self.__cost = cost
        self.__description = description

    # -------- Getters and Setters --------
    def getId(self): return self.__id
    def setId(self, id): self.__id = id

    def getType(self): return self.__type
    def setType(self, type): self.__type = type

    def getCost(self): return self.__cost
    def setCost(self, cost): self.__cost = cost

    def getDescription(self): return self.__description
    def setDescription(self, description): self.__description = description

    # -------- Métodos --------
    def addService(self):
        print(f"Service '{self.__type}' added. Cost: ${self.__cost}")

    def removeService(self):
        print(f"Service '{self.__type}' removed. Cost: ${self.__cost}")

    def showInfo(self):
        print(f"Service: {self.__type} - {self.__description} - ${self.__cost}")
