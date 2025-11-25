from employee import Employee

class Receptionist(Employee):
    def createReservation(self, reservation):
        print(f"Receptionist creating reservation #{reservation.getId()}...")
        super().createReservation(reservation)

    def modifyReservation(self, reservation, newCheckIn=None, newCheckOut=None):
        print(f"Receptionist modifying reservation #{reservation.getId()}...")
        super().modifyReservation(reservation, newCheckIn, newCheckOut)
