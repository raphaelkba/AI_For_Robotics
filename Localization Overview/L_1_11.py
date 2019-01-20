#Write code that outputs p after multiplying each entry 
#by pHit or pMiss at the appropriate places. Remember that
#the red cells 1 and 2 are hits and the other green cells
#are misses.


p=[0.2,0.2,0.2,0.2,0.2]
pHit = 0.6
pMiss = 0.2

#Enter code here
mult = [pMiss, pHit, pHit, pMiss, pMiss]
for i in range(len(p)):
    p[i] = p[i]*mult[i]
print (p)