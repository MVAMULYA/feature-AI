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
# Create a dictionary grid for the string
def grid_values(sudokustr):
    grid_dict={}
    for i in range(len(sudokustr)):
        grid_dict[boxes[i]] = sudokustr[i]
    return grid_dict
# Display SUDOKU grid
def display_grid(grid_b):
    width = 1 + max(len(grid_b[a]) for a in grid_b)
    line = '+'.join(['-'*(width*3)]*3)
    for c in columns:
        print(''.join(grid_b[c+r].center(width) + ('|' if r in '36' else '') for r in rows))
        if c in 'CF':
            print(line)
# Assign values for the blank box
def upgrade_grid(grid_b):
    for i in grid_b:
        if grid_b[i] == '.':
            grid_b[i] = '123456789'
    return grid_b
# Eliminate values of boxes that are available in peers
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
# Find the only choice available for a box and replace it with it
def only_choice(grid_b):
    for unit in units:
        for box in unit:
            if len(grid_b[box]) != 1:
                for digit in grid_b[box]:
                    possible_boxes = [boxes for boxes in unit if (digit in grid_b[boxes] and boxes != box)]
                    if len(possible_boxes) == 0:
                        grid_b[box] = digit
    return grid_b 
# Perform the eliminate, only_choice functions to reduce the possibilities
def reduce_puzzle(grid_b):
    stalled = False
    while not stalled:
        solved_values_before = [box for box in grid_b.keys() if len(grid_b[box]) == 1]
        #eliminate
        grid_b = eliminate(grid_b)
        #only_choice
        grid_b = only_choice(grid_b)
        solved_values_after = [box for box in grid_b.keys() if len(grid_b[box]) == 1]
        stalled = solved_values_before == solved_values_after
    return grid_b
sudostr = input("enter a sudoku string with 89 characters")
grid_boxes = grid_values(sudostr)
display_grid(grid_boxes)
grid_boxes = upgrade_grid(grid_boxes)
display_grid(grid_boxes)
grid_boxes = reduce_puzzle(grid_boxes)
print('solved')
display_grid(grid_boxes)
