class ServiceReservation:
    def __init__(self, id, date_time, customer, service):
        self.__id = id
        self.__date_time = date_time
        self.__customer = customer
        self.__service = service
        
    def getId(self): 
        return self.__id
    
    def getDateTime(self): 
        return self.__date_time
    
    def getCustomer(self): 
        return self.__customer
    
    def getService(self): 
        return self.__service
        
    def setDateTime(self, date_time): 
        self.__date_time = date_time
        
    def createReservation(self):
        self.__customer.makeServiceReservation(self)
        print(f"Service Reservation #{self.__id} created successfully for {self.__customer.getName()}")
        return True

    def showInfo(self):
        return (
            f"--- [SERVICE] Reservation #{self.__id} ---\n"
            f"  Customer: {self.__customer.getName()} ({self.__customer.getEmail()})\n"
            f"  Service: {self.__service.getType()} | Cost: ${self.__service.getCost():.2f}\n"
            f"  Requested Date/Time: {self.__date_time}"
        )