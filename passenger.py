class Passenger():
	def __init__(self, floor, destination):
		self.curfloor = floor
		self.destination = destination
		self.direction = 
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
	def _update_floor(self):
		self.curfloor = self.elevator.curfloor
	def update(self):
		self.update_floor()
		if self.curfloor==self.destination:
			self.leave_elevator()
