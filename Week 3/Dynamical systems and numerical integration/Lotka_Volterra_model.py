# Coursera - Simulation and modeling of natural processes - Dynamical systems

# Importing libraries
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Defining parameters
k_a = 1                         # reproduction rate of the antelopes
k_c = 1                         # death rate of cheetahs
k_ac = 0.5                      # death rate of antelopes when the meet cheetahs
k_ca = 0.5                      # reproduction rate of the cheetahs when they meet antelopes

del_t = 0.001                   # Interval taken
t_min = 0                       # Starting time
t_max = 30000                   # Ending time of simulation
t = np.zeros(t_max - t_min)
for i in range(0, len(t)):
    t[i] = i*del_t

P_a = np.zeros(len(t))          # Population of antelope at time t
P_a[0] = 2
P_c = np.zeros(len(t))          # Population of cheetahs at time t
P_c[0] = 3
dP_a = np.zeros(len(t))
dP_c = np.zeros(len(t))
C = 10                          # Total capacity of the population at any time
nu = 0.5

# Euler's Explicit scheme
for it in range(0, len(t) - 1):
    dP_a[it] = k_a*P_a[it] - k_ca*P_c[it]*P_a[it]               # Rate of change of population for antelope
    dP_c[it] = -1 * k_c * P_c[it] + k_ac * P_a[it] * P_c[it]    # Rate of change of population for cheetah
    P_a[it+1] = P_a[it] + del_t*dP_a[it]                        # Population of antelope at time t+1 based on time t
    P_c[it + 1] = P_c[it] + del_t * dP_c[it]                    # Population of cheetah at time t+1 based on time t

# Plotting the population of cheetahs and antelopes
plt.loglog(t, P_a, linewidth=2.0,label="Antelop population")
plt.loglog(t, P_c, linewidth=2.0,label="Cheetah population")
plt.legend()
plt.show()
