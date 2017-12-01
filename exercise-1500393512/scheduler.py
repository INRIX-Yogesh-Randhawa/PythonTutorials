class Scheduler:
    def __init__(self, edges, debug=False):
        self.__debug = debug
        self.__graph = dict({})
        self.__paths = []
        self.__stack = []

        for edge in edges:
            self.debug_print(edge)

            origin = edge['origin']
            destination = edge['destination']

            if origin not in self.__graph:
                self.__graph[origin] = dict({
                    'prev_links': [],
                    'next_links': []
                })

            self.__graph[origin]['next_links'].append(edge)

            if destination not in self.__graph:
                self.__graph[destination] = dict({
                    'prev_links': [],
                    'next_links': []
                })

            self.__graph[destination]['prev_links'].append(edge)

        self.debug_print('\n{}'.format(self.__graph))

    def schedule(self):
        for place in self.__graph:
            self.traverse_path(place)

        for place in self.__stack:
            self.traverse_path(place)

        bundles = []
        for paths in self.__paths:
            bundle = [link['id'] for link in paths]
            bundles.append(' '.join(bundle))

        return bundles

    def traverse_path(self, place):
        self.debug_print('\n\nTraversing with starting point {}'.format(place))

        self.traverse_backward(place)
        self.traverse_forward(place)

    def traverse_backward(self, current, day=None):
        backward_path = self.look_backward(current, day)

        if len(backward_path) != 0:
            self.debug_print('\nChecking any forward paths to merge')
            backward_path_reversed = list(reversed(backward_path))
            path_to_merge_index = -1
            for i, path in enumerate(self.__paths):
                link = path[0]
                last_link = backward_path[0]

                # self.debug_print('Compare {} {} {} {}'.format(last_link['destination'], last_link['day'], link['origin'],
                #                                          link['day']))

                if link['origin'] == last_link['destination'] and last_link['day'] == link['day'] - 1:
                    self.debug_print(
                        'Merging backward path {} with forward path {} at {}'.format(last_link['id'], link['id'],
                                                                                     link['origin']))
                    path_to_merge_index = i

            if path_to_merge_index >= 0:
                self.__paths[path_to_merge_index] = backward_path_reversed + self.__paths[path_to_merge_index]
            else:
                self.__paths.append(backward_path_reversed)

    def traverse_forward(self, current, day=None):
        forward_path = self.look_forward(current, day)

        if len(forward_path) != 0:
            self.debug_print('\nChecking any backward paths to merge')
            path_to_merge_index = -1
            for i, path in enumerate(self.__paths):
                link = path[-1]
                next_link = forward_path[0]

                # self.debug_print('Compare {} {} {} {}'.format(link['destination'], link['day'], next_link['origin'],
                #                                          next_link['day']))

                if link['destination'] == next_link['origin'] and next_link['day'] == link['day'] + 1:
                    self.debug_print(
                        'Merging forward path {} with backward path {} at {}'.format(next_link['id'], link['id'],
                                                                                     link['origin']))

                    path_to_merge_index = i

            if path_to_merge_index >= 0:
                self.__paths[path_to_merge_index] = self.__paths[path_to_merge_index] + forward_path
                self.debug_print('Merged Path: {}'.format(self.__paths[path_to_merge_index]))
            else:
                self.__paths.append(forward_path)

    def look_backward(self, current, day=None):
        path = []

        # don't look before MONDAY
        if day is not None and day == 0:
            return path

        # stop looking if no prev_links
        if not self.__graph[current]['prev_links']:
            return path

        self.debug_print('\nChecking backward path for {} on day {}'.format(current, day))

        edges_to_visit = []

        for edge in self.__graph[current]['prev_links']:
            if 'visited' in edge and edge['visited'] or day is not None and edge['day'] != day - 1:
                continue

            self.debug_print(edge)

            edges_to_visit.append(edge)

        if len(edges_to_visit) == 0:
            self.debug_print('No backward path from {} on day {}'.format(current, day and day - 1 or day))
            return path

        edge_in_path = edges_to_visit.pop(0)

        id = edge_in_path['id']
        name = edge_in_path['origin']
        day = edge_in_path['day']

        # mark backward link visited
        edge_in_path['visited'] = True

        path.append(edge_in_path)

        # mark forward link visited
        for edge in self.__graph[name]['next_links']:
            if edge['id'] == id:
                edge['visited'] = True

        self.debug_print('Path: {}'.format(path))

        path = path + self.look_backward(name, day)

        for edge in edges_to_visit:
            self.debug_print('Yet to visit {} {}'.format(edge['origin'], edge['id']))
            self.__stack.append(edge['origin'])

        return path

    def look_forward(self, current, day=None):
        path = []

        # don't look before MONDAY
        if day is not None and day == 4:
            return path

        # stop looking if no next_links
        if not self.__graph[current]['next_links']:
            return path

        self.debug_print('\nChecking forward path for {} on day {}'.format(current, day))

        edges_to_visit = []

        for edge in self.__graph[current]['next_links']:
            if 'visited' in edge and edge['visited'] or day is not None and edge['day'] != day + 1:
                continue

            self.debug_print(edge)

            edges_to_visit.append(edge)

        if len(edges_to_visit) == 0:
            self.debug_print('No forward path from {} on day {}'.format(current, day and day + 1) or day)
            return path

        edge_in_path = edges_to_visit.pop(0)

        id = edge_in_path['id']
        name = edge_in_path['destination']
        day = edge_in_path['day']

        # mark forward link visited
        edge_in_path['visited'] = True

        path.append(edge_in_path)

        # mark backward link visited
        for edge in self.__graph[name]['prev_links']:
            if edge['id'] == id:
                edge['visited'] = True

        self.debug_print('Path: {}'.format(path))

        path = path + self.look_forward(name, day)

        self.debug_print('Path: {}'.format(path))

        for edge in edges_to_visit:
            self.debug_print('Yet to visit {} {}'.format(edge['destination'], edge['id']))
            self.__stack.append(edge['destination'])

        return path

    def debug_print(self, *args):
        if self.__debug:
            print(*args)
