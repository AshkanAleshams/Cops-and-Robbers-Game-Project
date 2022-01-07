"""
Part 3: Visualising the traversal of the cop and the robber for each game.
"""
from __future__ import annotations
import networkx as nx
import matplotlib.pyplot as plt
import graph_vertex
import part1


def draw_paths(loaded_graph: graph_vertex.Graph, game: list,
               show_edges: bool = False, show_path_edges: bool = False) -> None:
    """
    This function is the main function for visualising the path of the cop and the robber. The
    output is an interactive plotly screen with a zooming-in-and-out feature.

    As there a lot of nodes in our graph, we have given users an option to decided whether they want
    to display the name of each location, the name of only the paths of the cop and the robber, or
    display no names at all.

    By default, the visualisation will not show the names of any nodes. If the user wants, they can
    specify their call as show_edges=True and/or show_path_edges=True, as per the three options
    described above.
    """
    # networkx requires a graph that made using the module.
    nx_graph = nx.Graph()  # initialing a Graph as a networkx Graph
    for v in loaded_graph.get_all_vertices():
        nx_graph.add_node(v)  # here we are manually adding each node of graph_vertex.Graph
        # to a networkx graph
    for e in loaded_graph.edges_list():  # edges_list() is defined in graph_vertex, check its
        # docstring for more information on how it works
        nx_graph.add_edge(e[0], e[1])  # this is to add each edge of the graph_vertex.Graph
        # to the networkx graph

    pos = nx.random_layout(nx_graph, seed=111)
    nx.draw(nx_graph, pos, node_color='black', node_size=0.5)
    path_robber = game[2]
    path_cop = game[1]
    # for i in range(len(game)):
    #     path_robber.append(game[2])
    #     path_cop.append(game[])
    path_edges1 = zip(path_robber, path_robber[1:])
    path_edges1 = set(path_edges1)
    path_edges2 = zip(path_cop, path_cop[1:])
    path_edges2 = set(path_edges2)
    nx.draw_networkx_nodes(nx_graph, pos, node_color='black', node_size=35)
    nx.draw_networkx_edges(nx_graph, pos, edgelist=path_edges1, edge_color='red', width=9)
    nx.draw_networkx_edges(nx_graph, pos, edgelist=path_edges2, edge_color='yellow', width=3)

    if show_edges is True:
        nx.draw_networkx_labels(nx_graph, pos, font_size=9, font_color='grey')

    elif show_path_edges is True and show_edges is False:
        edges = dict(path_edges1.union(path_edges2))
        nx.draw_networkx_labels(nx_graph, pos, labels=edges, font_size=14, font_color='#1059cc',
                                font_weight='heavy')

    plt.axis('equal')
    plt.show()


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
        'extra-imports': ['random', 'graph_vertex', 'part1', 'networkx', 'matplotlib.pyplot']
    })

    # Sample call

    # game_players = part1.initialize_robber_player('RobberPlayer', 'small_location_data.csv')
    # game_info = part1.run_game(robber_player=game_players[0], cop_player=game_players[1],
    #                            location_graph=game_players[2])
    #
    # # call to show the names of the nodes in the path of the robber or cop
    # draw_paths(game_players[2], game_info, show_path_edges=True)
