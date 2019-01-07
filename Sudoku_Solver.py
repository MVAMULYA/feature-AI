rows= '123456789'
columns = 'ABCDEFGHI'
def cross(row,col):
    listlen = []
    for c in col:
        for r in row:
            listlen.append(c+r)            
    return listlen
boxes = cross(rows,columns)
column_units = []
for r in rows:
    column_units.append(cross(r,columns))
row_units = []
for c in columns:
    row_units.append(cross(rows,c))    
square_units = []
rs = ['123','456','789']
cs = ['ABC','DEF','GHI']
for c in cs:
    for r in rs:
        square_units.append(cross(r,c))
units = row_units + column_units + square_units
peers = {}
peer_units = {}
for b in boxes:
    for a in units:
        if b in a:
            peer_units.setdefault(b,[])
            peer_units[b].append(a)
    peer_set= set(sum(peer_units[b],[]))
    peer_set.remove(b)
    peers.setdefault(b,[])
    peers[b] = list(peer_set)
def grid_values(sudokustr):
    grid_dict={}
    for i in range(len(sudokustr)):
        grid_dict[boxes[i]] = sudokustr[i]
    return grid_dict
sudostr = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
sudoku2 = '.13....48.....46.....87.......38...734.....829...25.......97.....46.....72....83.'
#'4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
grid_boxes = grid_values(sudoku2)
def display_grid(grid_b):
    width = 1 + max(len(grid_b[a]) for a in grid_b)
    line = '+'.join(['-'*(width*3)]*3)
    for c in columns:
        print(''.join(grid_b[c+r].center(width) + ('|' if r in '36' else '') for r in rows))
        if c in 'CF':
            print(line)
display_grid(grid_boxes)
def upgrade_grid(grid_b):
    for i in grid_b:
        if grid_b[i] == '.':
            grid_b[i] = '123456789'
upgrade_grid(grid_boxes)

def eliminate(grid_b):
    for i in grid_b:
        if len(grid_b[i]) == 1:
            for a in peers[i]:
                if len(grid_b[a]) == 1:
                    continue
                else:
                   grid_b[a] = grid_b[a].replace(grid_b[i],'')
        else:
            continue
    return grid_b
# This method is mentioned in udacity
#def only_choice(grid_b):
#   for digit in '123456789':
#        for unit in units:
#            tofill_boxes = [box for box in unit]            
#            possible_places = [box for box in tofill_boxes if digit in grid_b[box] ]
#            if len(possible_places) == 1 :
#                grid_b[possible_places[0]] = digit
#    return grid_b
def only_choice(grid_b):
    for unit in units:
        for box in unit:
            if len(grid_b[box]) != 1:
                for digit in grid_b[box]:
                    possible_boxes = [boxes for boxes in unit if (digit in grid_b[boxes] and boxes != box)]
                    if len(possible_boxes) == 0:
                        grid_b[box] = digit
    return grid_b    

def reduce_puzzle(grid_b):
    stalled = False
    while not stalled:
        solved_values_before = [box for box in grid_b if len(grid_b[box]) == 1]
        #eliminate
        grid_b = eliminate(grid_b)
        #only_choice
        grid_b = only_choice(grid_b)
        solved_values_after = [box for box in grid_b.keys() if len(grid_b[box]) == 1]
        stalled = solved_values_before == solved_values_after
        return grid_b

def solvedgrid(grid_b):
    unittest = True
    for unit in units:
        unitstring = ''.join(sorted(grid_b[box] for box in unit))
        if unitstring != '123456789':
            unittest = False
    return unittest


def search(grid_b):
    grid_b = reduce_puzzle(grid_b)
    if grid_b is False:
        return False
    if all([len(grid_b[box]) == 1 for box in boxes]):
        solved = solvedgrid(grid_b)
        if solved:
            return grid_b
        else:
            return False
    tobefilled = {grid_b[box]:box for box in boxes if len(grid_b[box]) != 1}
    min_item = min(tobefilled,key=len)
    box = tobefilled[min_item]
    for digit in grid_b[box]:
        gridcopy = grid_b.copy()
        gridcopy[box] = digit
        gridcopy = search(gridcopy)
        if gridcopy:
            return gridcopy
            

grid_boxes= search(grid_boxes)
print(solvedgrid(grid_boxes))
display_grid(grid_boxes)




                    
