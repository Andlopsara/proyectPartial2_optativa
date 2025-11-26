from employee import Employee

class Bellboy(Employee):
    def deliverKeys(self, room):
        pass

    def notifyStatus(self, room):
        print(f"Notifying status of room {room.getId()}: {room.getStatus()}")
