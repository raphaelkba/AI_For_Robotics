# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space


def search(grid,init,goal,cost):
    # ----------------------------------------
    # insert code here
    # ----------------------------------------
    not_visited =[]
    print("Grid")
    print(grid)
    print("Goal")
    print(goal)
    # create a list with nodes that can be visisted/ are not obstacles
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                not_visited.append([i, j])
    # list with the nodes on the fringe and is cost
    open_list = []
    open_list.append([0, init[0], init[1]])
    # list with node on the fringe
    open_list_ = []
    open_list_.append([init[0], init[1]])
    print("Open list")
    print(open_list)
    
    while(open_list):        
        open_list.sort() # sort list by cost
        open_list.reverse() # smallest cost at the end for poping
        current_item = open_list.pop() # gets the node with lowest cost
        print("current item loop:")
        print(current_item)
        open_list_.remove([current_item[1],current_item[2]])
        # checks if node was already visited
        if [current_item[1],current_item[2]] in not_visited:
            not_visited.remove([current_item[1],current_item[2]])
        # checks for goal
        if [current_item[1],current_item[2]] == goal:
            print("goal found")
            return current_item
        # checks neighbour nodes
        for action in delta:
            next_item = [current_item[1] + action[0], current_item[2] + action[1]] 
            # append nodes that have not been visited or are not already in the list
            if next_item in not_visited and next_item not in open_list_:
                open_list.append([current_item[0]+cost, next_item[0], next_item[1]])
                open_list_.append([next_item[0], next_item[1]])
    # returns fail
    print("No solution was found")
    return 'fail'



grid = [[0, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']
search(grid,init,goal,cost)