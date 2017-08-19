import numpy as np
class Elevator():
	CAPACITY = 10
	DIR_UP = 1
	DIR_DOWN = -1
	DIR_NONE = 0
    def __init__(self):
        self.direction = None
        self.dest_same = []
        self.dest_reverse = []
        self.curfloor = 1
        self.carrying = 0

    def add_passenger(self):
    	if self.carrying < Elevator.CAPACITY:
    	    self.carrying += 1
    	    return True
    	else:
    		return False

    def remove_passenger(self):
    	self.carrying -= 1

    def add_destination(self, floor):
    	if floor == self.curfloor:
    		return False
    	if self._same_direction(floor):
    		self.dest_same = sorted(list(set(self.dest_same.append(floor))))
    	else:
    		self.dest_reverse = sorted(list(set(self.dest_reverse.append(floor))))
    	return True

    def remove_destination(self):
    	assert self.direction != Elevator.DIR_NONE
    	if self.direction == Elevator.DIR_UP:
    		self.dest_same = self.dest_same[1:]
    	else: #self.direction == Elevator.DIR_DOWN:
    		self.dest_same = self.dest_same[:-1]


    def _same_direction(self, floor):
    	if self.direction==Elevator.DIR_NONE:
    		return True
    	if self.direction==Elevator.DIR_UP and floor > self.curfloor:
    		return True
    	if self.direction==Elevator.DIR_DOWN and floor < self.curfloor:
    		return True
    	return False