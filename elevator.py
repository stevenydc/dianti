from constants import *
class Elevator():
    '''
    Elevator controls the logic of elevator movements and passenger loading.
    It keeps track of # of passengers it carries (in real life this would be weight), and rejects passenger if full
    '''
    CAPACITY = 10
    def __init__(self):
        self.direction = DIR_NONE
        self.dest_same = [] # destinations that are down stream from current direction
        self.curfloor = 1
        self.carrying = 0
        self.state = STOPPED

    def add_passenger(self):
        if self.carrying < Elevator.CAPACITY:
            self.carrying += 1
            return True
        else:
            return False

    def remove_passenger(self):
        assert self.carrying > 0
        self.carrying -= 1

    def add_destination(self, floor):
        if floor == self.curfloor:
            return False
        if self._same_direction(floor):
            self.dest_same.append(floor)
            self.dest_same = sorted(list(set(self.dest_same)))
        else:
            raise ValueError('adding reverse destination is currently undefined behavior,\
                              current floor: {}, current direction: {}, requested_floor: {}'.format(self.curfloor, self.direction, floor))
        self.update_direction()
        return True

    def remove_destination(self):
        '''
        If the elevator is currently at one fo the destinations, remove that from the destination list
        '''
        assert self.direction != DIR_NONE
        if not self.dest_same:
            pass
        elif self.curfloor==self.dest_same[0]:
            self.dest_same.pop(0)
        elif self.curfloor==self.dest_same[-1]:
            self.dest_same.pop(-1)
        else:
            pass
        self.update_direction()

    def _same_direction(self, floor):
        '''
        Helper function.
        True if the elevator will pass by floor going in the current cirection
        '''
        if self.direction==DIR_NONE:
            return True
        if self.direction==DIR_UP and floor > self.curfloor:
            return True
        if self.direction==DIR_DOWN and floor < self.curfloor:
            return True
        return False

    #def _reverse_direction(self):
    #    assert self.direction!=DIR_NONE
    #    if self.direction == DIR_DOWN:
    #        self.direction = DIR_UP
    #    else: # self.direction == DIR_UP
    #        self.direction = DIR_DOWN

    def update_direction(self):
        '''
        Frequently called function. Updates the current direction that the elevator is moving in.
        Up, Down, or None
        '''
        if self.direction == DIR_NONE:
            if len(self.dest_same)==0:
                return
            self.direction = DIR_UP if self.dest_same[0]-self.curfloor>0 else DIR_DOWN
        elif len(self.dest_same) == 0:
            self.direction = DIR_NONE
        else: # Keep the same direction
            pass

    def move(self):
        if self.direction==DIR_DOWN:
            self.curfloor-=1
            self.remove_destination()
        elif self.direction==DIR_UP:
            self.curfloor+=1
            self.remove_destination()
        else:
            pass
