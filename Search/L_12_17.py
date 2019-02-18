# ----------
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def compute_value(grid,goal,cost):
    # ----------------------------------------
    # insert code below
    # ----------------------------------------
    value_grid = [[99 for col in range(len(grid[0]))] for row in range(len(grid))]
    stop = False # flag for stopping while loop
    
    while not stop:
        stop = True
        
        # goes through entire grid
        for x in reversed(range(len(grid))): # reversed since the goal its at the end of the grid
            for y in reversed(range(len(grid[0]))):
                # checks for goal
                if goal[0] == x and goal[1] == y:
                    if value_grid[x][y] > 0:
                        value_grid[x][y] = 0 #  goal has a 0 value
                        stop = False # sets flag
                elif grid[x][y] == 0:
                    #check every action
                    for action in delta:
                        next_item = [x + action[0], y + action[1]] 
                        if next_item[0] >= 0 and next_item[0] < len(grid) and next_item[1] >= 0 and next_item[1] < len(grid[0]) and grid[next_item[0]][next_item[1]] ==0:
                            new_value = value_grid[next_item[0]][next_item[1]] + cost
                            # checks if the path is shorter
                            if new_value < value_grid[x][y]:
                                value_grid[x][y] = new_value 
                                stop = False
        for i in range(len(value_grid)):
            print (value_grid[i])
        print('---------------------------')
    
    # make sure your function returns a grid of values as 
    # demonstrated in the previous video.
    return value_grid 
compute_value(grid,goal,cost)
