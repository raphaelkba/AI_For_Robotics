from math import *
from matrix import *

class ExtendedKalmanFilter(object):
    """
    Implementation of a extended kalman filter (EKF) for a bycicle model
    """
    
    def __init__(self):
        """ 
        Constructor of the Extended Kalman Filter for a nonlinear bycicle 
        model with 5 states and 2 inputs, which models approximatly the one 
        from robot class
        Inputs: a - acceleration and w - steering velocity
        States: x - x position
                y - y position
                theta - heading angle
                phi - steering angle
                v - velocity
            x_dot = [[d*cos(theta)],
                     [d*sin(theta)],
                     [phi],
                     [w],
                     [d_dot]]
        """
       # Initializes the EKF matrices
       # help parameters   
        self.dt = 1.0
        self.number_states = 5
        self.number_inputs = 2
        self.cov = 1000.0
        self.measureUncert = 10.0 # measurement uncertainty
       
       # initial states (x,y,theta,phi and v)
        self.x = matrix([[]])
        self.x.zero(self.number_states, 1) 
       
       # initial uncertainty matrix
        self.P = matrix([[self.cov, 0, 0, 0, 0],
                        [0, self.cov, 0, 0, 0],
                        [0, 0, self.cov, 0, 0],
                        [0, 0, 0, self.cov, 0],
                        [0, 0, 0, 0, self.cov]])
            
        # input
        self.u = matrix([[]])
        self.u.zero(self.number_states, 1)
        
        # State transition matrix
        self.F = matrix([[]])
        self.F.zero(self.number_states,self.number_states)
        
        # state measurement function
        self.H = matrix([[1.0, 0, 0, 0, 0],
                         [0, 1.0, 0, 0, 0]])
        
        # measurement uncertainty
        self.R = matrix([[self.measureUncert, 0],
                         [0,self.measureUncert]])
        
        # identity matrix
        self.I = matrix([[]])
        self.I.identity(self.number_states)
            
      
    def update(self, z):
        """
        updates the current belief and uncertainty matrix for the EKF
        input: measure values of x and y
        
        """
        y = z - self.H * self.x
        S = self.H * self.P * self.H.transpose() + self.R
        K = self.P * self.H.transpose() * S.inverse()
        self.x = self.x + K * y
        self.P = (self.I - K * self.H) * self.P
        return self.x.value[0][0], self.x.value[1][0]
    
    def predict(self):
        """
        predict step of the EKF
        output: x and y values prediction
        """
        v = self.x.value[4][0]
        theta = self.x.value[2][0]
        phi = self.x.value[3][0]
        angle = theta + phi
        F = matrix([[1.0, 0, -v*sin(angle)*self.dt, -v*sin(angle)*self.dt, cos(angle)*self.dt],
                     [0, 1.0, v*cos(angle)*self.dt, v*cos(angle)*self.dt, sin(angle)*self.dt],
                     [0, 0, 1.0, self.dt, 0],
                     [0, 0, 0, 1.0, 0],
                     [0, 0, 0, 0, 1.0]])
        
        self.x = self.bycicle_dynamics()
        self.P = F * self.P * F.transpose()
        
        return self.x.value[0][0], self.x.value[1][0]
        
    def bycicle_dynamics(self):
        x = self.x.value[0][0]
        y = self.x.value[1][0]
        theta = self.x.value[2][0]
        phi = self.x.value[3][0]
        v = self.x.value[4][0]
        phi = max(-pi, phi)
        phi = min( pi, phi)
        angle = self.angle_trunc(theta + self.dt* phi)
        bicycle = matrix([[x + self.dt * v * cos(angle)],
                       [y + self.dt * v * sin(angle)],
                       [angle],
                       [phi],
                       [v]])
        return bicycle
    
    def angle_trunc(self, a):
        """
        truncates angle between -pi and pi - function taken from robot class
        """
        while a < 0.0:
            a += pi * 2.0
        return ((a + pi) % (pi * 2)) - pi
         
    def predictAfterN(self, n):
        """
        Predicts the state of the variables based on the current estimations
        after n time steps, and return the x and y positions.

        Returns:
            x and y positions estimated to be after n time steps
        """
        x = self.bycicle_dynamics()
        for _ in range(n-1):
            x = self.bycicle_dynamics()
        return x.value[0][0], x.value[1][0]