from typing import List
from ant_system import Ant

# mostly just used for debugging...

def pprint_area(area):
    # assumes a square area
    n = len(area[0])
    print("start")
    print(" ↓ " + ' '.join(['_' for _ in range(n)]))
    print('\n'.join([' '.join(['|'] + ['X' if cell == 0 else ' ' for cell in row] + ['|']) for row in area]))
    print(' ' + ' '.join([' '.join(['‾' for _ in range(n)])] + ['ꜛ']))
    print(' '.join([' '.join([' ' for _ in range(n)])] + ['end']))

def pprint_area_with_moves(area, moves: List[tuple], current: tuple):
    n = len(area)
    # replace all blocked cells with X's, and all moves with m's
    # and if possible move is on a blocked cell, put a '!'
    print_area = [['X' if area[i][j] == 0 else ' ' for j in range(n)] for i in range(n)]
    for m in moves:
        if print_area[m[0]][m[1]] != 'X':
            print_area[m[0]][m[1]] = 'm'
        else:
            print_area[m[0]][m[1]] = '!'
    # print ants current position
    print_area[current[0]][current[1]] = 'A'
    print('\n'.join([' '.join(cell for cell in row) for row in print_area]))

def pprint_tour(area, ant: Ant):
    n = len(area)
    # replace all blocked cells with X's, and tour with dots
    print_area = [['X' if area[i][j] == 0 else ' ' for j in range(n)] for i in range(n)]
    for m in list(ant.tour_set):
        if print_area[m[0]][m[1]] != 'X':
            print_area[m[0]][m[1]] = '•'
        else:
            print_area[m[0]][m[1]] = '!'
    print('\n'.join([' '.join(cell for cell in row) for row in print_area]))