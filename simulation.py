
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
    return [w1, dw1, w2, dw2] 

# set the intial conditions and solve the equations of motion
# also need to define the time span for the simulation


# Time span for the simulation (0 to 20 seconds, 60 frames per second)
t_span = (0, 20)
t_eval = np.linspace(t_span[0], t_span[1], t_span[1] * 60)

# Initial conditions
# Angles are in radians. Let's start them almost horizontal.
initial_state_1 = [np.radians(120), 0, np.radians(-10), 0]  # [theta1, omega1, theta2, omega2]

# The second pendulum is offset by just 0.05 degrees!
offset = np.radians(0.05)
initial_state_2 = [initial_state_1[0] + offset, initial_state_1[1], initial_state_1[2] + offset, initial_state_1[3]]

# Solve the differential equations
sol1 = solve_ivp(double_pendulum_derivatives, t_span, initial_state_1, t_eval=t_eval, method='Radau')
sol2 = solve_ivp(double_pendulum_derivatives, t_span, initial_state_2, t_eval=t_eval, method='Radau')

# convert polar angles to cartesian coordinates for animation
def get_xy_coords(solution):
    th1 = solution.y[0]
    th2 = solution.y[2]
    
    # First bob (x1, y1)
    x1 = L1 * np.sin(th1)
    y1 = -L1 * np.cos(th1)
    
    # Second bob (x2, y2)
    x2 = x1 + L2 * np.sin(th2)
    y2 = y1 - L2 * np.cos(th2)
    
    return x1, y1, x2, y2

x1_a, y1_a, x2_a, y2_a = get_xy_coords(sol1)
x1_b, y1_b, x2_b, y2_b = get_xy_coords(sol2)

# animate the chaos
# use matplotlib.animation to draw the frames. I will draw Pendulum A in Blue, and Pendulum B in Red.

# Set up the figure
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-(L1 + L2 + 0.5), L1 + L2 + 0.5)
ax.set_ylim(-(L1 + L2 + 0.5), L1 + L2 + 0.5)
ax.set_aspect('equal')
ax.grid()
ax.set_title("Chaotic Double Pendulum\nRed is offset by 0.05° from Blue")

# Initialize the lines for the pendulums and their trails
line1, = ax.plot([],[], 'o-', color='blue', lw=2, markersize=6, label='Pendulum 1')
line2, = ax.plot([],[], 'o-', color='red', lw=2, markersize=4, label='Pendulum 2')
trail1, = ax.plot([],[], '-', color='blue', alpha=0.3, lw=1)
trail2, = ax.plot([],[], '-', color='red', alpha=0.3, lw=1)
ax.legend(loc="upper left")

# History length for the trails
trail_length = 30 

def animate(i):
    # Plot Pendulum 1
    line1.set_data([0, x1_a[i], x2_a[i]], [0, y1_a[i], y2_a[i]])
    # Plot Pendulum 2
    line2.set_data([0, x1_b[i], x2_b[i]], [0, y1_b[i], y2_b[i]])
    
    # Plot Trails (the paths of the bottom bobs)
    start_idx = max(0, i - trail_length)
    trail1.set_data(x2_a[start_idx:i], y2_a[start_idx:i])
    trail2.set_data(x2_b[start_idx:i], y2_b[start_idx:i])
    
    return line1, line2, trail1, trail2

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=len(t_eval), interval=1000/60, blit=True)

plt.show()