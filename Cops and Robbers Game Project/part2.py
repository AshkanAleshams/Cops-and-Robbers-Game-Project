"""
Part 2: Implementing the move algorithm, implementing the player classes
"""
from __future__ import annotations

import random
from typing import Union

import graph_vertex


################################################################################
# Cops and Robbers player classes
################################################################################
class Player:
    """Class representing a player"""

    def get_curr_location(self) -> graph_vertex.Vertex:
        """return the curr_location attribute"""
        raise NotImplementedError

    def get_move_count(self) -> int:
        """return the move_count attribute"""
        raise NotImplementedError

    def get_target_location(self) -> tuple[graph_vertex.Vertex, str]:
        """return the target_location attribute"""
        raise NotImplementedError

    def get_move_limit(self) -> int:
        """return the move_limit attribute"""
        raise NotImplementedError

    def update_location(self, new_location: graph_vertex.Vertex) -> None:
        """update the curr_location attribute"""
        raise NotImplementedError

    def add_move_count(self) -> None:
        """increase the move_count attribute by one"""
        raise NotImplementedError

    def update_target_location(self, target_location: tuple[graph_vertex.Vertex, str]) -> None:
        """Update the target_location attribute"""
        raise NotImplementedError

    def get_valid_path(self, location_graph: graph_vertex.Graph) -> list:
        """return a valid path for the player """
        raise NotImplementedError


class RobberPlayer(Player):
    """
    The class representing the Robber Player that priotizes the safest path of moves

    - target_location[1] in {'mid', 'end'}
    """
    curr_location: graph_vertex.Vertex
    move_limit: int
    move_count: int
    target_location: tuple[graph_vertex.Vertex, str]

    def __init__(self, curr_location: graph_vertex.Vertex,
                 target_location: tuple[graph_vertex.Vertex, str], move_limit: int = 20,
                 move_count: int = 0) -> None:
        """Initialize a new RiskyRobberPlayer with a current location, move count and move limit

        """
        self.curr_location = curr_location
        self.move_count = move_count
        self.move_limit = move_limit
        self.target_location = target_location

    def get_curr_location(self) -> graph_vertex.Vertex:
        """return the curr_location attribute"""
        return self.curr_location

    def get_move_count(self) -> int:
        """return the move_count attribute"""
        return self.move_count

    def get_target_location(self) -> tuple[graph_vertex.Vertex, str]:
        """return the target_location attribute"""
        return self.target_location

    def get_move_limit(self) -> int:
        """return the move_limit attribute"""
        return self.move_limit

    def update_location(self, new_location: graph_vertex.Vertex) -> None:
        """update the curr_location attribute"""
        self.curr_location = new_location

    def update_target_location(self, target_location: tuple[graph_vertex.Vertex, str]) -> None:
        """Update the target_location attribute"""
        self.target_location = target_location

    def add_move_count(self) -> None:
        """increase the move_count attribute by one"""
        self.move_count = self.move_count + 1

    def get_valid_path(self, location_graph: graph_vertex.Graph) -> list:
        """ return the shortest path of vertices with the least amount of unsafe locations
        (vertex score > 5) that the Player can make a move to
        if
        starting vertex is a neighbour of self.curr_location,
        starting vertex is connected to self.target_location,
        starting vertex.score <= 5

        >>> location_graph = graph_vertex.Graph()
        >>> location_graph.add_vertex(item = 'hi', kind='s', score=5 )
        >>> location_graph.add_vertex(item='hello', kind = 'h', score =7)
        >>> location_graph.add_vertex(item='bye',kind= 'p',score= 3)
        >>> location_graph.add_vertex(item='hey', kind='g',score= 4)
        >>> location_graph.add_vertex(item='lol', kind='g', score=4)
        >>> location_graph.add_edge('hi', 'hello') # v1 is a neighbour of v2
        >>> location_graph.add_edge('hello', 'bye') # v1 is a neighbour of v3
        >>> location_graph.add_edge('hi', 'hey')
        >>> location_graph.add_edge('hey', 'bye')
        >>> v1 = location_graph.vertices['hi']
        >>> v2 = location_graph.vertices['bye']
        >>> robber_player = RobberPlayer(v1, (v2, 'mid'))
        >>> robber_player.get_valid_path(location_graph) == ['hey', 'bye'] or ['bye', 'hey']
        ['bye', 'hey']
        """

        valid_path_so_far = []

        vertices = self.curr_location.neighbours

        for vertex in vertices:
            if vertex.check_connected(self.target_location[0].item, set())\
                    and vertex.score <= 5:
                path = location_graph.get_path(self.target_location[0].item, vertex.item)

                valid_path_so_far.append((count_vertices_greater_five(location_graph, path), path))

        return min(valid_path_so_far)[1]


class RiskyRobberPlayer(Player):
    """Class representing risky robber player that pritorizes the shortest path of moves
    """
    curr_location: graph_vertex.Vertex
    move_limit: int
    move_count: int
    target_location: tuple[graph_vertex.Vertex, str]

    def __init__(self, curr_location: graph_vertex.Vertex,
                 target_location: tuple[graph_vertex.Vertex, str], move_count: int = 0,
                 move_limit: int = 20) -> None:
        """Initialize a new RiskyRobberPlayer with a current location, move count and move limit

        """
        self.curr_location = curr_location
        self.move_count = move_count
        self.move_limit = move_limit
        self.target_location = target_location

    def get_curr_location(self) -> graph_vertex.Vertex:
        """return the curr_location attribute"""
        return self.curr_location

    def get_move_count(self) -> int:
        """return the move_count attribute"""
        return self.move_count

    def get_target_location(self) -> tuple[graph_vertex.Vertex, str]:
        """return the target_location attribute"""
        return self.target_location

    def update_target_location(self, target_location: tuple[graph_vertex.Vertex, str]) -> None:
        """Update the target_location attribute"""
        raise NotImplementedError

    def get_move_limit(self) -> int:
        """return the move_limit attribute"""
        return self.move_limit

    def update_location(self, new_location: graph_vertex.Vertex) -> None:
        """update the curr_location attribute"""
        self.curr_location = new_location

    def add_move_count(self) -> None:
        """increase the move_count attribute by one"""
        self.move_count += 1

    def get_valid_path(self, location_graph: graph_vertex.Graph) -> list:
        """ return the shortest path of vertices that the Player can make a move to
        the return is a list of vertex items
        if
        starting vertex is a neighbour of self.curr_location,
        starting vertex is connected to self.target_location,
        starting vertex.score =< 5

        >>> location_graph = graph_vertex.Graph()
        >>> location_graph.add_vertex(item = 'hi', kind='s', score=5 )
        >>> location_graph.add_vertex(item='hello', kind = 'h', score =7)
        >>> location_graph.add_vertex(item='bye',kind= 'p',score= 3)
        >>> location_graph.add_vertex(item='hey', kind='g',score= 4)
        >>> location_graph.add_vertex(item='lol', kind='g', score=4)
        >>> location_graph.add_edge('hi', 'hello') # v1 is a neighbour of v2
        >>> location_graph.add_edge('hello', 'hey') # v1 is a neighbour of v3
        >>> location_graph.add_edge('hey', 'bye')
        >>> location_graph.add_edge('hi', 'bye')
        >>> v1 = location_graph.vertices['hi']
        >>> v2 = location_graph.vertices['bye']
        >>> robber_player = RiskyRobberPlayer(v1, (v2, 'mid'))
        >>> robber_player.get_valid_path(location_graph)
        ['bye']
        """
        valid_path_so_far = []

        vertices = self.curr_location.neighbours

        for vertex in vertices:
            if (vertex.score <= 5) and \
                    (vertex.check_connected(self.target_location[0].item, set())):
                path = location_graph.get_path(self.target_location[0].item, vertex.item)
                valid_path_so_far.append((len(path), path))

        return min(valid_path_so_far)[1]


class CopPlayer:
    """Class representing the cop player
    """
    curr_location: graph_vertex.Vertex
    move_count: int

    def __init__(self, curr_location: graph_vertex.Vertex, move_count: int = 0) -> None:
        """Initialize a new RiskyRobberPlayer with a current location, move count and move limit

        """
        self.curr_location = curr_location
        self.move_count = move_count

    def make_move(self, location_graph: graph_vertex.Graph,
                  target_location: graph_vertex.Vertex) -> None:
        """Make a move based on the move_count, if move_count is divisalbe by 3, then we can
        make a move to a location with a score of less than 5, other wise it has to be >= 5."""

        if self.move_count % 3 == 0:
            vertices = self.curr_location.neighbours
            for vertex in vertices:
                if (vertex.score < 5) and \
                        (vertex.check_connected(target_location.item, {self.curr_location})):
                    self.curr_location = vertex
                    self.move_count += 1
        else:
            vertices = self.curr_location.neighbours
            for vertex in vertices:
                if (vertex.score >= 5) and \
                        (vertex.check_connected(target_location.item, {self.curr_location})):
                    self.curr_location = vertex
                    self.move_count += 1


def count_vertices_greater_five(location_graph: graph_vertex.Graph, path: list) -> int:
    """ Takes a path and returns the number of vertices that have a score greater than 5.
            """
    vert_count = 0
    for i in range(0, len(path)):
        vertex = location_graph.vertices[path[i]]
        if vertex.score > 5:
            vert_count += 1

    return vert_count


def choose_target_location(curr_location: graph_vertex.Vertex, visited: set[graph_vertex.Vertex],
                           location_graph: graph_vertex.Graph,
                           point_type: str) -> Union[None, tuple[graph_vertex.Vertex, str]]:
    """choose a node in the location_graph to be the target_location

    Preconditions:
        - point_type in {'mid', 'end'}
    """
    items = list(location_graph.get_all_vertices(''))

    for _ in range(1, len(items)):
        item = random.choice(items)
        target = location_graph.vertices[item]
        if target not in curr_location.neighbours \
                and target not in visited:
            return (target, point_type)

    return None


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'max-nested-blocks': 4,
        'disable': ['E1136', 'W0212'],
        'allowed-io': ['run_game', 'load_location_graph'],
        'extra-imports': ['random', 'graph_vertex']
    })
