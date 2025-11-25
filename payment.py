from datetime import date

class Payment:
    def __init__(self, id, amount, paymentMethod, reservation=None):
        self.__id = id
        self.__amount = amount
        self.__paymentMethod = paymentMethod
        self.__reservation = reservation
        self.__date = date.today()

    # -------- Getters and Setters --------
    def getId(self): return self.__id
    def setId(self, id): self.__id = id

    def getAmount(self): return self.__amount
    def setAmount(self, amount): self.__amount = amount

    def getPaymentMethod(self): return self.__paymentMethod
    def setPaymentMethod(self, method): self.__paymentMethod = method

    def getReservation(self): return self.__reservation
    def setReservation(self, reservation): self.__reservation = reservation

    def getDate(self): return self.__date

    # -------- Métodos --------
    def processPayment(self):
        print(f"Payment processed for ${self.__amount} by {self.__paymentMethod} on {self.__date}.")

    def cancelPayment(self):
        print(f"Payment #{self.__id} canceled.")

    def showPayment(self):
        print(f"Payment #{self.__id}: ${self.__amount}, method: {self.__paymentMethod}, date: {self.__date}")
