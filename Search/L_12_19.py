# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.


forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 0, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [0, 5] # given in the form [row,col]

cost = [2, 1, 13] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid,init,goal,cost):
    # intialize matrices, notice that for each orientation we should calculate the cost value
    value = [[[999 for row in range(len(grid[0]))] for col in range(len(grid))],
             [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
             [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
             [[999 for row in range(len(grid[0]))] for col in range(len(grid))]]
             
    policy = [[[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
              [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
              [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
              [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]]
    
    policy2D = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    
    stop = False
    
    while not stop:
        stop = True
        # go through all grid cells
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                # for each possible orientation cofiguration compute the value
                for orientation in range(len(forward)): # 4 possible orientation given by forward
                    # set goal to 0
                    if goal[0] == x and goal[1] == y:
                        if value[orientation][x][y] > 0:
                            value[orientation][x][y] = 0
                            policy[orientation][x][y] = '*'
                            stop = False # continue the while loop flag
                    
                    elif grid[x][y] == 0: # if the grid is empty
                        
                        # compute the three possible actions
                        for i in range(len(action)):
                            o_ = (orientation + action[i]) % len(forward) # orientation will give which way to go (which forward)
                            x_ = x + forward[o_][0]
                            y_ = y + forward[o_][1]
                            if x_ >= 0 and x_ < len(grid) and y_ >= 0 and y_ < len(grid[0]) and grid[x_][y_] ==0:
                                new_value = value[o_][x_][y_] + cost[i]
                                # update value
                                if new_value < value[orientation][x][y]:
                                    value[orientation][x][y] = new_value
                                    policy[orientation][x][y] = action_name[i]
                                    stop = False # while there is an update continue while loop
                                    
    x = init[0]
    y = init[1]
    orientation = init[2]
    policy2D[x][y] = policy[orientation][x][y] # initialize the starting position
    
    # Gets the optimal policy
    while policy[orientation][x][y] != '*':
        if policy[orientation][x][y] == '#':
            o_ = orientation
        elif policy[orientation][x][y] == 'R':
            o_ = (orientation - 1) % len(forward)
        elif policy[orientation][x][y] == 'L':
            o_ = (orientation + 1) % len(forward)
        x = x + forward[o_][0]
        y = y + forward[o_][1]
        orientation = o_
        policy2D[x][y] = policy[orientation][x][y]

    #return policy2D
    for i in range(len(policy2D)):
        print (policy2D[i])
    for i in range(len(value)):
        print (value[i])
optimum_policy2D(grid,init,goal,cost)

