# Modify class variable and stuff here
class PassengerGenerator():
	def __init__(self, floors, frequency):
		pass
	def generate(self):

class Simulator():
	def __init__(self, floors, num_elevators, frequency):
		self.floors = floors
		self.passengers=set()
		self.elevators = [Elevator() for i in range(num_elevators)]
		self.waiting_passengers = {floor:set() for floor in floors}
		self.command_sys = CommandSystem(floors, self.elevators)
		self.passenger_generator = PassengerGenerator(floors, frequency):
	def available_elevators(self, floor):
		output = []
		for elevator in self.elevators:
			if elevator.curfloor == floor:
				output.append(elevator)
	    return output

	def update(self):
		self.passenger_generator.generate()
		for floor in self.floors:
			if len(self.waiting_passengers[floor]) == 0:
				continue
			elevators = self.available_elevators(floor)
			for passenger in self.waiting_passengers[floor]:
				for elevator in elevators:
					if elevator.direction != passenger.direction:
						continue
					if passenger.enter_elevator(elevator):
						self.waiting_passengers[floor].pop(passenger)
						break
			



def set_up(num_elevators, )
if __name__=='__main__':
    pass
