from employee import Employee

class Receptionist(Employee):
    def createReservation(self, reservation):
        super().createReservation(reservation)

    def modifyReservation(self, reservation, newCheckIn=None, newCheckOut=None):
        super().modifyReservation(reservation, newCheckIn, newCheckOut)
