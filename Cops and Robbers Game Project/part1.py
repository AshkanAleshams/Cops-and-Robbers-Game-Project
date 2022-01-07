"""Part 1
Part 1: Loading the data-set, adding the nodes to the city, creating random edges, ensuring that
there is path between the start, the mid and the end(escape)
"""
from __future__ import annotations
import csv
import graph_vertex
import part2


def load_location_graph(data_file: str) -> graph_vertex.Graph:
    """Will load a location graph using a data file and assign a score to each vertex

    """
    score_dict = {'park': 3, 'cemetery': 0, 'health': 7, 'fire station': 3,
                  'police station': 10, 'tourist spot': 5}

    location_graph = graph_vertex.Graph()

    with open(data_file, 'r') as file:
        reader = csv.reader(file)

        for location in reader:
            location_score = score_dict[location[1]]
            location_graph.add_vertex(item=location[0], kind=location[1], score=location_score)

    location_graph.assign_random_edges()

    return location_graph


def randomize_start(location_graph: graph_vertex.Graph) -> list:
    """Given a location_graph, return a list of 2 suitable start positions based on the number of
    neighbours the vertex has.

    >>> location_graph = graph_vertex.Graph()
    >>> location_graph.add_vertex(item = 'hi', kind='s', score=5 )
    >>> location_graph.add_vertex(item='hello', kind = 'h', score =7)
    >>> location_graph.add_vertex(item='bye',kind= 'p',score= 6)
    >>> location_graph.add_vertex(item='hey', kind='g',score= 7)
    >>> location_graph.add_vertex(item='lol', kind='g', score=9)
    >>> location_graph.add_edge('hi', 'hello') # v1 is a neighbour of v2
    >>> location_graph.add_edge('hi', 'bye') # v1 is a neighbour of v3
    >>> location_graph.add_edge('lol', 'hey')
    >>> location_graph.add_edge('hi', 'hey')
    >>> randomize_start(location_graph)[0].item
    'hi'
    >>> randomize_start(location_graph)[1].item
    'hey'

    """
    vertices_so_far = []
    for item in location_graph.get_all_vertices(''):
        vertex = location_graph.vertices[item]

        vertices_so_far.append((vertex.degree(), vertex.item))

    vertices_so_far.sort(reverse=True)
    return [location_graph.vertices[vertices_so_far[0][1]],
            location_graph.vertices[vertices_so_far[1][1]]]


def initialize_robber_player(player: str, data: str) -> list:
    """Initialize a new robber player by setting the start location and target location
    Preconditions:
      - player in {'RobberPlayer', 'RiskyRobberPlayer'}
    """
    location_graph = load_location_graph(data)
    start_locations = randomize_start(location_graph)
    cop_start = start_locations[1]

    cop_player = part2.CopPlayer(cop_start)

    rob_start = start_locations[0]

    rob_target_location = part2.choose_target_location(rob_start, set(), location_graph, 'mid')

    if player == 'RobberPlayer':
        return [part2.RobberPlayer(curr_location=rob_start, target_location=rob_target_location),
                cop_player, location_graph]

    if player == 'RiskyRobberPlayer':
        return [part2.RiskyRobberPlayer(curr_location=rob_start,
                                        target_location=rob_target_location),
                cop_player, location_graph]


# def run_game(player: str, data: str) -> list:
#     """run the game with given robber player and cop player and return the winner as well as
#     the paths of robber and cops
#
#     Precondition:
#         - player in {'RobberPlayer', 'RiskyRobberPlayer'}
#     """
    #
    # robber_path = robber_player.get_valid_path(location_graph)
    #
    # cop_path = []
    #
    # for i in range(1, len(robber_path)):
    #     robber_player.update_location(robber_path[i])
    #     robber_player.add_move_count()  # add 1 move to the move_count
    #
    #     # Make moves for cop
    #     cop_path.append(cop_player.curr_location)
    #     cop_player.make_move(location_graph, robber_player.get_target_location()[0])
    #     if robber_player.get_target_location()[0].item == robber_player.get_curr_location():
    #         if robber_player.get_target_location()[1] == 'end':
    #             print('The Robber Wins!')
    #             print([1, cop_path, robber_path])
    #             return [1, cop_path, robber_path]
    #
    #         elif robber_player.get_target_location()[1] == 'mid':
    #             new_target = part2.choose_target_location(robber_player.get_curr_location(),
    #                                                       {robber_player.get_curr_location()},
    #                                                       location_graph, 'end')
    #
    #             robber_player.update_target_location(new_target)
    #
    #             # Recurse
    #             run_game(robber_player, cop_player, location_graph)
    #
    #     if robber_player.get_curr_location() == cop_player.curr_location:
    #         print('The r2 Wins!')
    #         print([0, cop_path, robber_path])
    #         return [0, cop_path, robber_path]
    #
    #     if robber_player.get_move_count() == robber_player.get_move_limit():
    #         print('The r1 Wins!')
    #         print([0, cop_path, robber_path])
    #         return [0, cop_path, robber_path]
    #
    # # if we get to the end and no one wins
    # print('The Cop Wins!')
    # return [0, cop_path, robber_path]

def run_game(robber_player: part2.Player, cop_player: part2.CopPlayer,
             location_graph: graph_vertex.Graph) \
        -> list:
    """run the game with given robber player and cop player and return the winner as well as
    the paths of robber and cops

    Precondition:
        - player in {'RobberPlayer', 'RiskyRobberPlayer'}
    """

    robber_path = robber_player.get_valid_path(location_graph)

    cop_path = []

    for i in range(1, len(robber_path)):
        robber_player.update_location(robber_path[i])
        robber_player.add_move_count()  # add 1 move to the move_count

        # Make moves for cop
        cop_path.append(cop_player.curr_location.item)
        cop_player.make_move(location_graph, robber_player.get_target_location()[0])

        if robber_player.get_target_location() == robber_player.get_curr_location():
            if robber_player.get_target_location()[1] == 'end':
                print('The Robber Wins!')
                print([1, cop_path, robber_path])
                return [1, cop_path, robber_path]

            elif robber_player.get_target_location()[1] == 'mid':
                new_target = part2.choose_target_location(robber_player.get_curr_location(),
                                                          {robber_player.get_curr_location()},
                                                          location_graph, 'end')

                robber_player.update_target_location(new_target)

                # Recurse
                run_game(robber_player, cop_player, location_graph)

        if robber_player.get_curr_location() == cop_player.curr_location:
            print('The Cop Wins!')
            print([0, cop_path, robber_path])
            return [0, cop_path, robber_path]

        if robber_player.get_move_count() == robber_player.get_move_limit():
            print('The Cop Wins!')
            print([0, cop_path, robber_path])
            return [0, cop_path, robber_path]

    # if we get to the end and no one wins
    # print('The Cop Wins!')
    # print([0, cop_path, robber_path])
    print('oops you have reached the end of the for loop')
    return [0, cop_path, robber_path]


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'max-nested-blocks': 4,
        'disable': ['E1136', 'W0212', 'R1710'],
        'allowed-io': ['run_game', 'load_location_graph'],
        'extra-imports': ['random', 'csv', 'graph_vertex', 'part2']
    })
