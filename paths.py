def search(graph, path, last=None):
    dead_end = True
    last_link = None
    last_day = None

    if last is None and len(path) != 0:
        last_link = path[-1]
        last = last_link['destination']
        last_day = last_link['day']

    print('Last - {}'.format(last_link))

    for link in graph[last]:
        print(link, link['day'], last_day)
        if 'visited' not in link and (last_day is None or link['day'] == last_day + 1):
            dead_end = False
            link['visited'] = True
            path.append(link)
            print('Path Before. {}'.format(path))
            yield from search(graph, path)
            print('Path After. {}'.format(path))
            path.clear()
    if dead_end:
        print('Dead End. Path {}'.format(path))
        yield list(path)


def paths(graph, v):
    yield from search(graph, [], v)


vertices = ['SEA', 'PDX', 'DEN', 'SFO', 'KSC']
edges = [
    dict({
        'origin': 'SEA',
        'destination': 'PDX',
        'day': 0,
        'id': 1
    }),
    dict({
        'origin': 'SEA',
        'destination': 'DEN',
        'day': 3,
        'id': 22
    }),
    dict({
        'origin': 'PDX',
        'destination': 'SFO',
        'day': 1,
        'id': 2
    }),
    dict({
        'origin': 'PDX',
        'destination': 'DEN',
        'day': 1,
        'id': 3
    }),
    dict({
        'origin': 'DEN',
        'destination': 'SEA',
        'day': 2,
        'id': 44
    }),
    dict({
        'origin': 'DEN',
        'destination': 'KSC',
        'day': 4,
        'id': 99
    })
]

# graph = {'SEA': ['PDX', 'DEN'], 'PDX': ['SFO', 'DEN'], 'DEN': ['SEA', 'KSC'], 'SFO': [], 'KSC': []}

graph = dict({})

for v in vertices:
    graph[v] = []
    for e in edges:
        if e['origin'] == v:
            graph[v].append(e)

for n, e in graph.items():
    print('\n{} - {}'.format(n, e))
    for path in (paths(graph, n)):
        print(' '.join([str(p['id']) for p in path]))

