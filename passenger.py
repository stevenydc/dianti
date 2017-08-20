from constants import DIR_UP, DIR_DOWN, DIR_NONE
class Passenger():
    def __init__(self, floor, destination):
        self.curfloor = floor
        self.destination = destination
        self.direction = DIR_UP if destination > floor else DIR_DOWN
        self.elevator = None
        self.wait_time = 0
    def enter_elevator(self, elevator):
        assert elevator.curfloor == self.curfloor
        if not elevator.add_passenger():
            return False
        self.elevator = elevator
        self.elevator.add_destination(self.destination)
        return True
    def leave_elevator(self):
        self.elevator.remove_passenger()
        self.elevator = None

    def update(self):
        if self.elevator:
            self.curfloor = self.elevator.curfloor
        self.wait_time += 1


