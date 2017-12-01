import argparse
from scheduler import Scheduler

DAYS = dict({'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4})


def parse_line(line):
    shipment = line.split(' ')
    return dict({'id': shipment[0], 'origin': shipment[1], 'destination': shipment[2], 'day': DAYS[shipment[3]]})


def process(lines, debug):
    shipments = [parse_line(line) for line in lines]

    scheduler = Scheduler(shipments, debug)

    result = scheduler.schedule()

    scheduler.debug_print('\nOutput: Length - {}'.format(len(result)))

    return result


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
        debug = args.debug

        with open(args.input_file_path) as f:
            lines = f.read().splitlines()

            print('\n'.join(process(lines, debug)))
    except OSError:
        print('Error: Cannot open file \'{}\' for reading'.format(args.input_file_path))
    except Exception as e:
        print('Error: Error during process. {}'.format(e.args[0]))
        raise


if __name__ == '__main__':
    main()
