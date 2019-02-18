# ----------
# Part Four
#
# Again, you'll track down and recover the runaway Traxbot. 
# But this time, your speed will be about the same as the runaway bot. 
# This may require more careful planning than you used last time.
#
# ----------
# YOUR JOB
#
# Complete the next_move function, similar to how you did last time. 
#
# ----------
# GRADING
# 
# Same as part 3. Again, try to catch the target in as few steps as possible.

from robot import *
from math import *
from matrix import *
import random
from ExtendedKalmanFilter import ExtendedKalmanFilter

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    # This function will be called after each time the target moves. 

    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.
    steer_control = 0
    vel_control = 0
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        diff_heading = 0
        int_heading = 0 
        max_distance = 0 
        int_distance = 0
        count = 1
        kalman_filter_other = ExtendedKalmanFilter()        
        do_serach = True
        OTHER = [measurements, hunter_positions, hunter_headings, diff_heading, int_heading, max_distance, int_distance, count, kalman_filter_other, target_measurement] # now I can keep track of history
        predicted_measurement = target_measurement
    else: # not the first time, update my history

        # extended kalman filter
        measure = matrix([
                [target_measurement[0]],
                [target_measurement[1]]
                ])
        
#        if OTHER[7]%2 == 0:
        predicted_measurement = OTHER[8].predict()
        predicted_measurement = OTHER[8].update(measure)
            
    
#            if distance_between(hunter_position, target_measurement) > max_distance:
        next_step = OTHER[8].bycicle_dynamics()
        predicted_measurement = [next_step.value[0][0],next_step.value[1][0]]
#        else:
#            predicted_measurement = OTHER[8].update(measure)
#            predicted_measurement = OTHER[9]
            
        OTHER[9] = predicted_measurement
        predited_distance = distance_between(hunter_position, predicted_measurement)

        distance = min(predited_distance, max_distance)
        heading_to_target = get_heading(hunter_position, predicted_measurement)

        heading_difference = (heading_to_target - hunter_heading + 2*pi)%(2*pi)

        p_gain_steer = 1.0
        p_gain_vel = 1.0

        steer_control = p_gain_steer*(heading_difference)
        vel_control = p_gain_vel*(distance)
    
#        predited_distance1 = distance_between(hunter_position, predicted_measurement) 
#        predited_distance2 = distance_between(hunter_position, target_measurement)
#        print("Predict1")
#        print(predicted_measurement)
#        OTHER[8].x = OTHER[8].bycicle_dynamics()
#        predicted_measurement = [next_step.value[0][0],next_step.value[1][0]]

#        do_serach = False
##        if OTHER[7] >= round(OTHER[9]/10):
##        do_serach = True
#        if do_serach:
#            dim_x = 2000
#            dim_y = 2000
#            init = [round(10*(hunter_position[0] + 10)), round(10*(hunter_position[1] + 10))]
#            goal = [round(10*(predicted_measurement[0] + 10)), round(10*(predicted_measurement[1] + 10))]
#            path = search(create_grid(dim_x, dim_y),init,goal)
#            OTHER[9] = len(path)
#            previous_distance = distance_between(hunter_position, predicted_measurement)
#            found = False
#            k = 0
#            while not found:
#                
#                planned_measurement = path[k]
#                planned_measurement = [predicted_measurement[0]/10 - 10, predicted_measurement[1]/10 - 10]
#                
#                planned_distance = distance_between(planned_measurement, predicted_measurement)     
#                distance = min(planned_distance,max_distance)
#            
#                heading_to_target = get_heading(hunter_position, predicted_measurement)
#                heading_difference = (heading_to_target - hunter_heading + 2*pi)%(2*pi)
#        
#                p_gain_steer = 1.0
#                p_gain_vel = 1.0
#        
#                steer_control = p_gain_steer*(heading_difference)
#                vel_control = p_gain_vel*(distance)
#                
#                r = robot(hunter_position[0], hunter_position[1], hunter_heading)
#                r.move(steer_control, vel_control)
#                robot_distance = [r.x, r.y]
#                current_distance = distance_between(robot_distance,predicted_measurement)
#                k += 1
#                if  current_distance < previous_distance:
#                    previous_distance = current_distance
#                else:
#                    found = True
##                do_serach = False
#                
#            predited_distance = distance_between(hunter_position, predicted_measurement)
#            if predited_distance < max_distance:
#                distance = min(predited_distance, max_distance)
#                heading_to_target = get_heading(hunter_position, predicted_measurement)
#                heading_difference = (heading_to_target - hunter_heading + 2*pi)%(2*pi)
#        
#                p_gain_steer = 1.0
#                p_gain_vel = 1.0
#        
#                steer_control = p_gain_steer*(heading_difference)
#                vel_control = p_gain_vel*(distance)
#        else:



            
#        OTHER = list(OTHER)

        OTHER[3] = heading_difference
        OTHER[4] += heading_difference
        OTHER[5] = max_distance
        OTHER[6] += max_distance
        OTHER[7] += 1
    return steer_control, vel_control, OTHER, predicted_measurement

def create_grid(dim_x, dim_y):
    grid = [[0 for col in range(dim_y)] for row in range(dim_x)]
    return grid
    
    
    
def search(grid,init,goal):
    # ----------------------------------------
    # modify code below
    # ----------------------------------------
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    deltas = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    path_ = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    path = []
    closed[init[0]][init[1]] = 1
    cost = 1

    delta =[[-1,  0], # go up
            [-1,  -1], # up left 
            [ 0, -1], # go left
            [ 1, -1], # down left
            [ 1,  0], # go down
            [ 1,  1], # down right
            [ 0,  1], # go right
            [ -1, 1]]# up right
    
    x = init[0]
    y = init[1]
    g = 0

    open = [[g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find expand

    while not found and not resign:
        if len(open) == 0:
            resign = True
            return 0
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
            
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            # checks if it is going straight ir diagonally
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            closed[x2][y2] = 1
                            deltas[x2][y2] = i
#    path[goal[0]][goal[1]] = '*'
    
    path_[goal[0]][goal[1]] = '*'
    x = goal[0]
    y = goal[1]
    delta_name = ['^','^<', '<','v<','v','v>','>','^>']
    while [x,y] != [init[0],init[1]]:
        x_ = x - delta[deltas[x][y]][0]
        y_ = y - delta[deltas[x][y]][1]
        path_[x_][y_] = delta_name[deltas[x][y]]
        path.append([x_, y_])
        x = x_ 
        y = y_
    path.pop()
#    for i in range(len(path)):
#        print (path_[i])
    
#    x = goal[0]
#    y = goal[1]
#    while [x,y] != [init[0],init[1]]:
#        x_ = x - delta[deltas[x][y]][0]
#        y_ = y - delta[deltas[x][y]][1]
#        
#        x = x_ 
#        y = y_ 
#    print(path)
    return path # make sure you return the shortest path    
        

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 0.98 * target_bot.distance # 0.98 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0

    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        if separation < separation_tolerance:
            print ("You got it right! It took you ", ctr, " steps to catch the target.")
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER, yo = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)
        
        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()

        ctr += 1            
        if ctr >= 1000:
            print ("It took too many steps to catch the target.")
    return caught

def demo_grading2(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 0.98 * target_bot.distance # 0.98 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0
    #For Visualization
    import turtle
    window = turtle.Screen()
    window.bgcolor('white')
    chaser_robot = turtle.Turtle()
    chaser_robot.shape('arrow')
    chaser_robot.color('blue')
    chaser_robot.resizemode('user')
    chaser_robot.shapesize(0.3, 0.3, 0.3)
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.3, 0.3, 0.3)
    size_multiplier = 15.0 #change size of animation
    chaser_robot.hideturtle()
    chaser_robot.penup()
    chaser_robot.goto(hunter_bot.x*size_multiplier, hunter_bot.y*size_multiplier-100)
    chaser_robot.showturtle()
    broken_robot.hideturtle()
    broken_robot.penup()
    broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-100)
    broken_robot.showturtle()
    measuredbroken_robot = turtle.Turtle()
    measuredbroken_robot.shape('circle')
    measuredbroken_robot.color('red')
    measuredbroken_robot.penup()
    measuredbroken_robot.resizemode('user')
    measuredbroken_robot.shapesize(0.1, 0.1, 0.1)
    predicted_robot = turtle.Turtle()
    predicted_robot.shape('circle')
    predicted_robot.color('black')
    predicted_robot.penup()
    predicted_robot.resizemode('user')
    predicted_robot.shapesize(0.1, 0.1, 0.1)
    broken_robot.pendown()
    chaser_robot.pendown()
    #End of Visualization
    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:
        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        print("separation")
        print(separation)
        if separation < separation_tolerance:
            print ("You got it right! It took you ", ctr, " steps to catch the target.")
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER, predicted_measurement = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)

        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()
        #Visualize it
        measuredbroken_robot.setheading(target_bot.heading*180/pi)
        measuredbroken_robot.goto(target_measurement[0]*size_multiplier, target_measurement[1]*size_multiplier-100)
        measuredbroken_robot.stamp()
        predicted_robot.setheading(hunter_bot.heading*180/pi)
        predicted_robot.goto(predicted_measurement[0]*size_multiplier, predicted_measurement[1]*size_multiplier-100)    
        broken_robot.setheading(target_bot.heading*180/pi)
        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-100)
        chaser_robot.setheading(hunter_bot.heading*180/pi)
        chaser_robot.goto(hunter_bot.x*size_multiplier, hunter_bot.y*size_multiplier-100)

        #End of visualization
        ctr += 1            
        if ctr >= 1000:
            print ("It took too many steps to catch the target.")
    return caught

def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position

    heading = atan2(target_y - hunter_y, target_x - hunter_x)

    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!
    return turning, distance, OTHER

target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5)
measurement_noise = .05*target.distance
target.set_noise(0.0, 0.0, measurement_noise)
hunter = robot(-10.0, -10.0, 0.0)
#print (demo_grading(hunter, target, next_move))
print (demo_grading2(hunter, target, next_move))




