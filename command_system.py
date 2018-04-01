from constants import DIR_UP, DIR_DOWN, DIR_NONE
from elevator import Elevator
class CommandSystem():
    '''
    Keeps track of busy/idle elevators and distribute floor requests to elevators
    '''
    def __init__(self, floors, elevators):
        self.elevators={
            'busy':[],
            'idle':elevators
        }
        # If a floor request is mapped to True, it is being processed
        # Otherwise it is yet to be assigned to an elevator
        self.floor_requests = {}

    def _assign_elevator(self, request):
        '''
        input: tuple, (floor, direction)
        output: True if successfully assigned request to one elevator, False otherwise
        
        Tries to assign the request to one of the elevators, starting with the busy
        elevators that are going to pass by first.
        '''
        for elevator in self.elevators['busy']:
            if elevator.direction != request[1]:
                continue
            if elevator.curfloor > request[0] and request[1]==DIR_DOWN:
                elevator.add_destination(request[0])
                return True
            elif elevator.curfloor < request[0] and request[1]==DIR_UP:
                elevator.add_destination(request[0])
                return True
            else:
                # Among currently busy elevators, none is going to 'pass' the requested floor
                continue
        if len(self.elevators['idle']) > 0:
            self.elevators['idle'][0].add_destination(request[0])
            return True
        return False

    def process_floor_requests(self):
        '''Assigns elevators to each floor's each type of request'''
        for request in self.floor_requests:
            if self.floor_requests[request]:
                continue
            self.update_elevators()
            if self._assign_elevator(request):
                self.floor_requests[request] = True

    def add_floor_request(self, floor, direction):
        if (floor, direction) not in self.floor_requests:
            self.floor_requests[(floor, direction)] = False

    def update_elevators(self):
        '''
        Updates the busy/idle lists of elevators
        Deletes floor requests that are completed
        '''
        busy = []
        idle = []
        for elevator in self.elevators['busy']+self.elevators['idle']:
            if (elevator.curfloor, elevator.direction) in self.floor_requests:
                #if not self.floor_requests[(elevator.curfloor, elevator.direction)]:
                #    print("Unprocessed floor request is being completed")
                self.floor_requests.pop((elevator.curfloor, elevator.direction))
            if elevator.direction == DIR_NONE:
                idle.append(elevator)
            else:
                busy.append(elevator)
        self.elevators = {'busy':busy, 'idle':idle}


