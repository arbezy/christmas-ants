import heapq
from typing import List, Tuple, Optional

# NOTE: will need modifying to handle floats if maze has valyes between 0 and 1.
def astar(maze: List[List[int]]) -> Optional[List[Tuple[int, int]]]:
    """
    Find the shortest path through a grid maze using A* alg. 
    
    Returns a list of positions from start to end, if None if no route is possible.
    """
    rows, cols = len(maze), len(maze[0])
    n = len(maze) - 1
    start, goal = (0,0), (n,n)

    def abs_difference(pos: Tuple[int, int]) -> int:
        return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])

    # priority queue: (fitness=absolute distance from goal, g_score=length of current path , position, path)
    frontier = [(abs_difference(start), 0, start, [start])]
    visited = set()

    while frontier:
        f_score, g_score, current, path = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return path
        
        x, y = current
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 0 and (nx, ny) not in visited):
                new_g = g_score + 1
                new_f = new_g + abs_difference((nx, ny))
                heapq.heappush(frontier, (new_f, new_g, (nx, ny), path + [(nx, ny)]))

    return None