
# importing useful libraries

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import solve_ivp

# defining constants / physics parmaters
g = 9.81 # acceleration due to gravity (m/s^2)
L1 = 1.0 # length of first arm (m)
L2 = 1.0 # length of second arm (m)
m1 = 1.0 # mass of first bob (kg)
m2 = 1.0 # mass of second bob (kg)

# defining the equations of motion for the double pendulum

def double_pendulum_derivatives(t, state):
    # unpack the state: theta1, omega1, theta2, omega2
    th1, w1, th2, w2 = state

    delta = th2 - th1

    # equations of motion derived from Lagrangian mechanics
    # for a double pendulum system

    den1 = (2*m1+m2) - m2 * np.cos(2*delta)
    den2 = (2*m1+m2) - m2 * np.cos(2*delta)

    num1 = -g * (2 * m1 + m2) * np.sin(th1) - m2 * g * np.sin(th1 - 2 * th2) \
           - 2 * np.sin(delta) * m2 * (w2**2 * L2 + w1**2 * L1 * np.cos(delta))
    dw1 = num1 / (L1 * den1)
    
    num2 = 2 * np.sin(delta) * (w1**2 * L1 * (m1 + m2) + g * (m1 + m2) * np.cos(th1) \
           + w2**2 * L2 * m2 * np.cos(delta))
    dw2 = num2 / (L2 * den2)
    
    # Return
    return 

