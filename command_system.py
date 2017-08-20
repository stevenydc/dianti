from constants import DIR_UP, DIR_DOWN, DIR_NONE
from elevator import Elevator
class CommandSystem():
    def __init__(self, floors, elevators):
        self.elevators={
            'busy':[],
            'idle':elevators
        }
        self.floor_requests = {}

    def _assign_elevator(self, request):
        '''request is a tuple (floor, DIR_UP or DIR_DOWN)'''
        # TOOD: some how balance the load of busy elevators if multiple are available to take the request
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
            if self._assign_elevator(request):
                self.floor_requests[request] = True


    def add_floor_request(self, floor, direction):
        if (floor, direction) not in self.floor_requests:
            self.floor_requests[(floor, direction)] = False

    def update_elevators(self):
        #TODO: update busy and idle lists. depending on the elevator's direction
        busy = []
        idle = []
        for elevator in self.elevators['busy']+self.elevators['idle']:
            if (elevator.curfloor, elevator.direction) in self.floor_requests:
                if not self.floor_requests[(elevator.curfloor, elevator.direction)]:
                    print("Weird... unprocessed floor request is being completed?")
                    from IPython import embed
                    embed()
                self.floor_requests.pop((elevator.curfloor, elevator.direction))
            if elevator.direction == DIR_NONE:
                idle.append(elevator)
            else:
                busy.append(elevator)
        self.elevators = {'busy':busy, 'idle':idle}


