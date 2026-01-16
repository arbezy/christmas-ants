from typing import List

# NOTE: impl using Galler-Fischer tree
# src: https://en.wikipedia.org/wiki/Disjoint-set_data_structure
class DS:
    # NOTE: tried to flatten and it was a painnn
    def __init__(self, area: List[List[int]]):
        n = len(area)
        self.parent = [[(i,j) for j in range(n)] for i in range(n)]
        self.size = [[1] * n] * n

    # find set representative (roott of the tree in this case)
    # TODO: implement path splitting or halving instead
    def find(self, x: tuple[int,int]) -> tuple[int,int]:
        if self.parent[x[0]][x[1]] != x:
            self.parent[x[0]][x[1]] = self.find(self.parent[x[0]][x[1]])
            return self.parent[x[0]][x[1]]
        else:
            return x
        
    # union by size
    def union(self, x: tuple[int,int], y: tuple[int,int]):
        # replace nodes by roots
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return # return early as x and y are already in the same set !
        
        # if necessary swap the vars so that x has at least as many descendants as y
        if self.size[x[0]][x[1]] < self.size[y[0]][y[1]]:
            x, y = y, x

        # make x the new root / parent of y
        self.parent[y[0]][y[1]] = x
        # update the size of x
        self.size[x[0]][x[1]] = self.size[x[0]][x[1]] + self.size[y[0]][y[1]]

