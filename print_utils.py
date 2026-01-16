

# mostly just used for debugging...

def pprint_area(area):
    # assumes a square area
    n = len(area[0])
    print("start")
    print(" ↓ " + ' '.join(['_' for _ in range(n)]))
    print('\n'.join([' '.join(['|'] + ['X' if cell == 0 else ' ' for cell in row] + ['|']) for row in area]))
    print(' ' + ' '.join([' '.join(['‾' for _ in range(n)])] + ['ꜛ']))
    print(' '.join([' '.join([' ' for _ in range(n)])] + ['end']))
