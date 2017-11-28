import argparse

debug = False

DAYS = dict({'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4})

class Scheduler:
    def __init__(self, shipments):
        self.__network = dict({})
        self.__paths = []
        self.__stack = []

        for shipment in shipments:
            debug_print(shipment)

            id = shipment['id']
            origin = shipment['origin']
            destination = shipment['destination']
            day = shipment['day']

            if origin not in self.__network:
                self.__network[origin] = dict({
                    'origins': [],
                    'destinations': []
                })

            self.__network[origin]['destinations'].append(dict({
                'id': id,
                'name': destination,
                'day': DAYS[day]
            }))

            if destination not in self.__network:
                self.__network[destination] = dict({
                    'origins': [],
                    'destinations': []
                })

            self.__network[destination]['origins'].append(dict({
                'id': id,
                'name': origin,
                'day': DAYS[day]
            }))

        debug_print('\n{}'.format(self.__network))

    def schedule(self):
        for place in self.__network:
            self.traverse_path(place)

        bundles = []
        for paths in self.__paths:
            bundle = [link['id'] for link in paths]
            bundles.append(' '.join(bundle))

        return bundles

    def traverse_path(self, place):
        debug_print('\nTraversing with starting point {}'.format(place))

        backward_path = self.look_backward(place)

        day = None

        if len(backward_path) != 0:
            last = backward_path[len(backward_path) - 1]
            day = last['day']

        forward_path = self.look_forward(place, day)

        path = backward_path + forward_path

        if len(backward_path + forward_path) != 0:
            self.__paths.append(path)

    def look_backward(self, current, day=None):
        path = []

        # don't look before MONDAY
        if day is not None and day == DAYS['M']:
            return path

        # stop looking if no origins
        if not self.__network[current]['origins']:
            return path

        debug_print('Checking backward path for {} on day {}'.format(current, day))

        origins_to_visit = []

        for origin in self.__network[current]['origins']:
            debug_print(origin)

            if 'visited' in origin and origin['visited'] or day is not None and origin['day'] != day - 1:
                continue

            origins_to_visit.append(origin)

        if len(origins_to_visit) == 0:
            return path

        origin = origins_to_visit.pop(0)

        id = origin['id']
        name = origin['name']
        day = origin['day']

        debug_print('Adding {} to path'.format(name))

        path.append(dict({
            'id': id,
            'origin': name,
            'destination': current,
            'day': day
        }))

        # mark backward link visited
        origin['visited'] = True

        # mark forward link visited
        for destination in self.__network[name]['destinations']:
            if destination['name'] == current:
                destination['visited'] = True

        self.__stack.append(origin)

        backward_path = self.look_backward(name, day)

        for origin in origins_to_visit:
            debug_print('Yet to visit {} {}'.format(origin['name'], origin['id']))
            # self.traverse_path(origin['name']);

        path = backward_path + path

        debug_print(path)

        return path

    def look_forward(self, current, day=None):
        path = []

        # don't look before MONDAY
        if day is not None and day == DAYS['F']:
            return path

        # stop looking if no destinations
        if not self.__network[current]['destinations']:
            return path

        debug_print('Checking forward path for {} on day {}'.format(current, day))

        destinations_to_visit = []

        for destination in self.__network[current]['destinations']:
            debug_print(destination)

            if 'visited' in destination and destination['visited'] or day is not None and destination['day'] != day + 1:
                continue

            destinations_to_visit.append(destination)

        if len(destinations_to_visit) == 0:
            return path

        destination = destinations_to_visit.pop(0)

        id = destination['id']
        name = destination['name']
        day = destination['day']

        debug_print('Adding {} to path'.format(name))

        path.append(dict({
            'id': id,
            'origin': current,
            'destination': name,
            'day': day
        }))

        # mark backward link visited
        destination['visited'] = True

        # mark forward link visited
        for origin in self.__network[name]['origins']:
            if origin['name'] == current:
                origin['visited'] = True

        self.__stack.append(destination)

        forward_path = self.look_forward(name, day)

        for destination in destinations_to_visit:
            debug_print('Yet to visit {} {}'.format(destination['name'], destination['id']))

        path = path + forward_path

        debug_print(path)

        return path


def debug_print(*args):
    global debug
    if debug:
        print(*args)


def parse_line(line):
    shipment = line.split(' ')
    return dict({'id': shipment[0], 'origin': shipment[1], 'destination': shipment[2], 'day': shipment[3]})


def process(lines):
    shipments = [parse_line(line) for line in lines]

    debug_print(shipments)

    scheduler = Scheduler(shipments)
    return scheduler.schedule()


def main():
    try:
        parser = argparse.ArgumentParser(description='Convoy V1 scheduler')
        parser.add_argument('input_file_path', help='Input File Path')
        parser.add_argument('--debug', help='Run code with debug statements', action='store_true')

        args = parser.parse_args()
    except:
        print('Error: Please provide an input file path')
        raise

    try:
        global debug
        debug = args.debug

        with open(args.input_file_path) as f:
            lines = f.read().splitlines()

            debug_print('Input: {}'.format(lines))

            result = process(lines)

            debug_print('\nOutput: Length - {}'.format(len(result)))

            print('\n'.join(result))
    except OSError:
        print('Error: Cannot open file \'{}\' for reading'.format(args.input_file_path))
    except Exception as e:
        print('Error: Error during process. {}'.format(e.args[0]))


if __name__ == '__main__':
    main()
