import random
from typing import List

from disjoint_set import DS

def create_area(n: int):
    # 0 = traversable, 1 == not traversable
    # NOTE: in the future I'll make this a float to signify 'speed' of traversal

    # all cells start NOT traversable
    area = [[0 for _ in range(n)] for _ in range(n)]

    # select start point and end point at top left and bottom right
    area[0][0] = 1
    area[n-1][n-1] = 1

    # using a disjoint set to verify start and end connect, each cell starts as its own set
    # we then get a union of free adjacent cell sets and when a cell itself becomes free
    disjoint = DS(area)

    # while start and end are not in the same set, make a random cell traversable
    while disjoint.find((0,0)) != disjoint.find((n-1,n-1)):
        disjoint, area = traverse_random_cell(disjoint, area, n)

    return area

def traverse_random_cell(disjoint: DS, area: List[List[int]], n: int):
    # pick a random cell that is not traversable and make it traversable
    i, j = random.randint(0, n-1), random.randint(0, n-1)
    # NOTE: I could make this more efficient by makeing a list or set of all not traversable cells,
    # and taking random items from that collection so that we never end up choosing an already
    # traversable cell
    if area[i][j] == 0:
        area[i][j] = 1

        # look for clear neighbours 
        clear_neighbours = []
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for d in directions:
            neighbour = (i + d[0], j + d[1])
            # check if neighbour is within bounds and clear
            if neighbour[0] >= 0 and neighbour[0] < n and neighbour[1] >= 0 and neighbour[1] < n:
                if area[neighbour[0]][neighbour[1]] == 1:
                    clear_neighbours.append(neighbour)
        
        # replace their sets with a union of the 2 sets
        for c_n in clear_neighbours:
            disjoint.union((i,j), c_n)

    return disjoint, area

def weight_area(area: List[List[int]]) -> List[List[float]]:
    return [
        [float(c) * random.random() for c in row]
        for row in area
    ]