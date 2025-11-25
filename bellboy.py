from employee import Employee

class Bellboy(Employee):
    def deliverKeys(self, room):
        print(f"Delivery key for room {room.getId()} delivered to the customer.")

    def notifyStatus(self, room):
        print(f"Notifying status of room {room.getId()}: {room.getStatus()}")
