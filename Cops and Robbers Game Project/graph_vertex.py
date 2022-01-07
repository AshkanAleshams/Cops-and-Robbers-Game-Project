"""
The Graph and Vertex Class for Cops and Robbers. Some of the code in this file is based on code
that we've seen in the Course Notes, lectures and tutorials. Any method that is not from the
Course Notes is explained in its own docstring.
This file is Copyright (c) 2021 Aamishi Avarsekar, Ashkan Alesham, Harry Doung, Dravin Nagalingam
"""

from __future__ import annotations
import random
from typing import Any


class Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The name of the location stored in this vertex.
        - neighbours: The vertices that are adjacent to this vertex.
        - kind: the kind of location
        - score: a score from 1 to 10 inclusive given to the location

    Preconditions:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours) # self should be a neighbour to all of
        - kind in {'store', 'food', 'financial services',
        'automobile services', 'emergency services', 'park', 'school'}
    """
    item: str
    neighbours: set[Vertex]
    kind: str
    score: int

    def __init__(self, item: Any, kind: str, score: int) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'store', 'food', 'financial services',
        'automobile services', 'emergency services', 'park', 'school'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()
        self.score = score

    def degree(self) -> int:
        """
        Return the degree of this vertex. The degree of a vertex is defined as the number of its
        neighbours.
        >>> v1 = Vertex('Citi Field' ,'tourist spot', 5)
        >>> v2 = Vertex('Citi Field' ,'tourist spot', 4)
        >>> v3 = Vertex('Owls Head Park' ,'park', 3)
        >>> v1.neighbours = {v2, v3}
        >>> v1.degree()
        2
        """
        return len(self.neighbours)

    def check_connected(self, target_item: Any, visited: set[Vertex]) -> bool:
        """Return whether this vertex is connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited
        """
        if self.item == target_item:
            # Our base case: the target_item is the current vertex
            return True
        else:
            visited.add(self)  # Add self to the set of visited vertices
            for u in self.neighbours:
                if u not in visited:  # Only recurse on vertices that haven't been visited
                    if u.check_connected(target_item, visited):
                        return True

            return False

    def connected_distance(self, target_item: Any, visited: set[Vertex]) -> \
            any:
        """Return a path that connects self and target_item with length d.
        Return None if no such path is found or d == 0.

        Preconditions:
            - d >= 0
        """
        if self.item == target_item:
            return [self.item]

        else:
            visited.add(self)  # Add self to the list of visited vertices
            for u in self.neighbours:
                if u not in visited:  # cuts off access to visited in u has already been
                    path = u.connected_distance(target_item, visited)
                    # recurse wherever the return type is expected
                    if path is not None:
                        return [self.item] + path

            return None


class Graph:
    """A class that represents a graph.
    *This class has been adopted from the Course Notes and as seen in lectures and tutorials. Any
    method that is not from the Course Notes is explained in its own docstring.*
    """

    vertices: dict[Any, Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, item: Any, kind: str, score: int) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'park', 'cemetery', 'health', 'fire station',
                       'police station', 'tourist spot'}
        """
        if item not in self.vertices:
            self.vertices[item] = Vertex(item, kind, score)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self.vertices:
            v = self.vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'park', 'cemetery', 'health', 'fire station',
                       'police station', 'tourist spot'}

        *This function is adopted from Assignment 3, but modified as per the requirements of our
        project. The locations in the doctstring are picked from the dataset mentioned in the
        report*

        >>> g = Graph()
        >>> g.add_vertex('Citi Field' ,'tourist spot', 5)
        >>> g.add_vertex('Fort Tryon Park' ,'tourist spot', 4)
        >>> g.add_vertex('Owls Head Park' ,'park', 3)
        >>> g.get_all_vertices('tourist spot') == {'Citi Field', 'Fort Tryon Park'} or \
                                                {'Fort Tryon Park', 'Citi Field'}
        True
        >>> g.get_all_vertices('park')
        {'Owls Head Park'}
        """
        if kind != '':
            return {v.item for v in self.vertices.values() if v.kind == kind}
        else:
            return set(self.vertices.keys())

    def edges_list(self) -> list:
        """
        Print a list of all the edges in a graph. An edge is represented by a size 2 tuple of each
        of its vertex.

        >>> g = Graph()
        >>> g.add_vertex('Citi Field' ,'tourist spot', 5)
        >>> g.add_vertex('Fort Tryon Park' ,'tourist spot', 4)
        >>> g.add_vertex('Owls Head Park' ,'park', 3)
        >>> g.add_edge('Citi Field', 'Owls Head Park')
        >>> g.add_edge('Citi Field', 'Fort Tryon Park')
        >>> g.edges_list() == [('Citi Field', 'Fort Tryon Park'), \
                               ('Citi Field', 'Owls Head Park')] or \
                               [('Citi Field', 'Owls Head Park'), ('Citi Field', 'Fort Tryon Park')]
        True
        """
        edges_list = []
        for u1 in self.vertices.values():
            for u2 in self.vertices.values():
                if self.adjacent(u1.item, u2.item):
                    if (u1.item, u2.item) and (u2.item, u1.item) not in edges_list:
                        edges_list.append((u1.item, u2.item))
        return edges_list

    def assign_random_edges(self) -> None:
        """
        Takes vertices in the graph and randomly assigns edges.
        The purpose of this function is to replicate an arbitrary graph with random edges formed by
        its set of vertices.
        """
        vertices = list(self.vertices)
        edges = set()
        counter = 300

        curr = random.choice(vertices)

        while counter != 0:
            vert1 = random.choice(vertices)
            if curr != vert1:
                self.add_edge(curr, vert1)
                if {curr, vert1} not in edges:
                    edges.update({curr, vert1})
            curr = vert1
            counter -= 1

    def get_path(self, item1: Any, item2: Any) -> list:
        """Return the shortest path between item1 and item 2 in this graph.

        The returned list contains the ITEMS along the path.
        Return None if no such path exists.

        >>> g = Graph()
        >>> g.add_vertex('Citi Field' ,'tourist spot', 5)
        >>> g.add_vertex('Fort Tryon Park' ,'tourist spot', 4)
        >>> g.add_vertex('Owls Head Park' ,'park', 3)
        >>> g.add_edge('Citi Field', 'Owls Head Park')
        >>> g.add_edge('Owls Head Park', 'Fort Tryon Park')
        >>> g.get_path('Citi Field', 'Fort Tryon Park')
        ['Citi Field', 'Owls Head Park', 'Fort Tryon Park']
        """

        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            for _ in range(1, len(self.vertices)):
                path = v1.connected_distance(item2, set())
                if path is not None:
                    return path
        return []


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'max-nested-blocks': 4,
        'disable': ['E1136'],
        'extra-imports': ['random']
    })
