"""
Part 4: Analysis of Player AI
"""
from __future__ import annotations
import plotly.graph_objects as go
import part1


def run_multiple_games(n: int, robber_player: str, data: str) -> any:
    """will run multiple games and output a plot

    Preconditions:
        - robber_player in {'RobberPlayer', 'RiskyRobberPlayer'}
    """
    rob_wins_so_far = 0

    for _ in range(0, n):
        game_players = part1.initialize_robber_player(robber_player, data)
        result = part1.run_game(robber_player=game_players[0], cop_player=game_players[1],
                                location_graph=game_players[2])

        rob_wins_so_far += result[0]

    labels = ['Cop', 'Robber']
    values = [n - rob_wins_so_far, rob_wins_so_far]

    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, title=f'Winnings of Cops vs {robber_player}')])
    fig.show()


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
        'extra-imports': ['graph_vertex', 'part1', 'networkx', 'plotly.graph_objects']
    })
