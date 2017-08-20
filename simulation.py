# Modify class variable and stuff here
import numpy as np
import random
import time
from constants import DIR_UP, DIR_DOWN, DIR_NONE
from passenger import Passenger
from elevator import Elevator
from command_system import CommandSystem

class PassengerGenerator():
    def __init__(self, floors, l):
        '''
        floors is a list of numbers representing the floors
        l can be a float or an array of floats
         - if float, then passengers of all floors are generated the same way
         - if array, then each floor uses the specific Lambda provided in the array
        l = average number of people arriving at the elevator lobby on each floor in 10 seconds
        '''
        self.l = {floor:l for floor in floors} if isinstance(l, float) else {floor:l for floor,l in zip(floors, l)} # Lambda of the Poisson process
        self.floors = set(floors)

    def destination_generator(self, start_floor):
        self.floors.discard(start_floor)
        destination = random.sample(self.floors,1)[0]
        self.floors.add(start_floor)
        return destination

    def generate(self):
        new_passengers = {
            floor: {
                Passenger(floor, self.destination_generator(floor)) 
                for i in range(np.random.poisson(self.l[floor]))
            }
            for floor in self.floors
        }
        return new_passengers

class Simulator():
    def __init__(self, floors, num_elevators, load):
        self.passengers_served = 0
        self.floors = floors
        self.passengers=set()
        self.elevators = [Elevator() for i in range(num_elevators)]
        self.waiting_passengers = {floor:set() for floor in floors}
        self.command_sys = CommandSystem(floors, self.elevators)
        self.passenger_generator = PassengerGenerator(floors, load)

    def available_elevators(self, floor):
        output = []
        for elevator in self.elevators:
            if elevator.curfloor == floor:
                output.append(elevator)
        return output

    def generate_new_passengers(self):
        new_passengers = self.passenger_generator.generate()
        for floor in self.waiting_passengers:
            self.waiting_passengers[floor].update(new_passengers[floor])
            self.passengers.update(new_passengers[floor])

    def update_floor_requests(self):
        for floor, passengers in self.waiting_passengers.items():
            for passenger in passengers:
                self.command_sys.add_floor_request(floor, passenger.direction)


    def update(self):
        # Spawn new passegners
        self.generate_new_passengers()
        # let passengers leave elevators first
        discard = set()
        for passenger in self.passengers:
            if not passenger.elevator:
                continue
            if passenger.curfloor == passenger.destination:
                passenger.leave_elevator()
                self.passengers_served += 1
                discard.add(passenger)
        self.passengers -= discard

        # let passengers in the lobby to get into elevators
        for floor in self.floors:
            if len(self.waiting_passengers[floor]) == 0:
                continue
            elevators = self.available_elevators(floor)
            discard = set()
            for passenger in self.waiting_passengers[floor]:
                for elevator in elevators:
                    if elevator.direction == passenger.direction or elevator.direction==DIR_NONE:
                        if passenger.enter_elevator(elevator):
                            discard.add(passenger)
                            break
                    else:
                        continue
            self.waiting_passengers[floor] -= discard
        self.command_sys.update_elevators()
        self.update_floor_requests()
        self.command_sys.process_floor_requests()
        self.command_sys.update_elevators()
        for elevator in self.elevators:
            elevator.move()
        for passenger in self.passengers:
            passenger.update()
    def print_visualize(self):
        floor_elevators = {floor:False for floor in self.floors}
        for elevator in self.elevators:
            floor_elevators[elevator.curfloor]=True
        floor_passenger = {floor:{DIR_UP:0, DIR_DOWN:0} for floor in self.floors}
        for floor in self.waiting_passengers:
            for passenger in self.waiting_passengers[floor]:
                floor_passenger[floor][passenger.direction]+=1

        print('Total Number of Passengers Served:', self.passengers_served)
        print('Elevator 1 destinations: {}'.format(self.elevators[0].dest_same))
        print('Elevator 2 destinations: {}'.format(self.elevators[1].dest_same))

        direction_map = {DIR_DOWN:'v', DIR_UP:'^', DIR_NONE:'-'}
        for idx in range(len(self.floors)-1, -1, -1):
            floor = self.floors[idx]
            string = ""
            for elevator in self.elevators:
                if elevator.curfloor==floor:
                    string+='|{}{:>2}|'.format(direction_map[elevator.direction],elevator.carrying)
                else:
                    string+='|   |'
            string += '^'*floor_passenger[floor][DIR_UP]
            string += 'v'*floor_passenger[floor][DIR_DOWN]
            print(string)

    def start_game(self):
        while True:
            self.update()
            self.print_visualize()
            input()







if __name__=='__main__':
    floors = list(range(1,11))
    num_elevators = 2
    load = 0.05
    my_sim = Simulator(floors, num_elevators, load)
    my_sim.start_game()
