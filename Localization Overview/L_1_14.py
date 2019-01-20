#Modify your code so that it normalizes the output for 
#the function sense. This means that the entries in q 
#should sum to one.
import math

p=[0.2, 0.2, 0.2, 0.2, 0.2]
world=['green', 'red', 'red', 'green', 'green']
Z = 'red'
pHit = 0.6
pMiss = 0.2
sum_prob = 0.0

def sense(p, Z):
    q=[]
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    sum_prob = math.fsum(q) # sum(q) also works
    for i in range(len(q)):
        q[i] = q[i]/sum_prob
        
    return q
print (sense(p,Z))