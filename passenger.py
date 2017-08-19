class passenger():
	def __init__(self, floor, destination):
		self.curfloor = floor
		self.destination = destination
		self.elevator = None
	def enter_elevator(self, elevator):
		self.elevator = elevator
	def leave_elevator(self, elevator):
		self.elevator.remove_passenger()
		self.elevator = None
	def update_floor(self):
		self.curfloor = self.elevator.curfloor