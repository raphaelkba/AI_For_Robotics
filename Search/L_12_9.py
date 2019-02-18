# -----------
# User Instructions:
# 
# Modify the function search so that it returns
# a table of values called expand. This table
# will keep track of which step each node was
# expanded.
#
# Make sure that the initial cell in the grid 
# you return has the value 0.
# ----------


def search(grid,init,goal,cost):
    # ----------------------------------------
    # modify code below
    # ----------------------------------------
    not_visited =[]
    expand = [[0 for row in range(len(grid[1]))] for col in range(len(grid))]
    print("Grid")
    print(grid)
    print("Goal")
    print(goal)
    # create a list with nodes that can be visisted/ add obstacles to expand list
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                not_visited.append([i, j])
                expand[i][j] = 0
            else:
                expand[i][j] = -1
    # list with the nodes on the fringe and is cost
    open_list = []
    open_list.append([0, init[0], init[1]])
    # list with node on the fringe
    open_list_ = []
    open_list_.append([init[0], init[1]])
    print("Open list")
    print(open_list)
    counter = 1
    while(open_list):        
        open_list.sort() # sort list by cost
        open_list.reverse() # smallest cost at the end for poping
        current_item = open_list.pop() # gets the node with lowest cost
        print("current item loop:")
        print(current_item)
        expand[current_item[1]][current_item[2]] = counter
        counter += 1
        open_list_.remove([current_item[1],current_item[2]])
        # checks if node was already visited
        if [current_item[1],current_item[2]] in not_visited:
            not_visited.remove([current_item[1],current_item[2]])
        # checks for goal
        if [current_item[1],current_item[2]] == goal:
            print("goal found")
            for i in range(len(expand)):
                for j in range(len(expand[0])):
                    if expand[i][j] == 0:
                        expand[i][j] = -1
                    elif expand[i][j] != -1:
                        expand[i][j] -= 1

            return expand
        # checks neighbour nodes
        for action in delta:
            #print("Current action")
            #print(action)
            next_item = [current_item[1] + action[0], current_item[2] + action[1]] 
#            print("Next item")
#            print(next_item)
            # append nodes that have not been visited or are not already in the list
            if next_item in not_visited and next_item not in open_list_:
                open_list.append([current_item[0]+cost, next_item[0], next_item[1]])
                open_list_.append([next_item[0], next_item[1]])
    for i in range(len(expand)):
        for j in range(len(expand[0])):
            if expand[i][j] == 0:
                expand[i][j] = -1
            elif expand[i][j] != -1:
                expand[i][j] -= 1    
    return expand

grid = [[0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 1, 0],
        [0, 0, 1, 1, 0, 1, 1],
        [0, 0, 0, 1, 0, 0, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']
print(search(grid,init,goal,cost))