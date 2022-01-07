"""CSC111 Winter 2021 Final Project
by Aamishi Avarsekar, Ashkan Alesham, Harry Doung, Dravin Nagalingam

This is the main runner for this project


Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 David Liu and Isaac Waller.
"""
import part3
import part4
import part1


def run_program(n: int, robber_player: str, data: str) -> None:
    """Will run the program by running n number of games, visualize the total result
    and visualize one of the games.

    Preconditions:
        - robber_player in {'RobberPlayer', 'RiskyRobberPlayer'}"""

    part4.run_multiple_games(n, robber_player, data)

    game_players = part1.initialize_robber_player(robber_player, data)
    game_info = part1.run_game(robber_player=game_players[0], cop_player=game_players[1],
                               location_graph=game_players[2])

    # call to show the names of the nodes in the path of the robber or cop
    part3.draw_paths(game_players[2], game_info, show_path_edges=True)


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
        'extra-imports': ['part1', 'part4', 'part3']
    })
