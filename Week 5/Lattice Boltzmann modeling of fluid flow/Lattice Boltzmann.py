# Coursera - Simulation and modeling of natural processes - Lattice Boltzmann modeling of fluid flow

# Importing libraries
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm

# Defining parameters
# Flow parameters
t_iter = 10       # Total number of iterations
nx = 400            # Number of nodes along X
ny = 100            # Number of nodes along Y
h = ny - 1          # Height of domain

cx = nx/4           # X co-ordinate of body (cylinder)
cy = ny/2           # Y co-ordinate of body

Re = 10             # Reynold's number
r = ny/9            # Radius of body
uL = 0.04           # Characteristic length of body
nuL = uL*r/float(Re)    # viscosity
omega = 1/float(3*nuL+0.5)  # Relaxation parameter

col1 = np.array([0,1,2])    # Define column 1
col2 = np.array([3,4,5])    # Define column 2
col3 = np.array([6,7,8])    # Define column 3

obstacle = (nx-cx)**2+(ny-cy)**2 < r**2

# Lattice parameters
v = np.array([ [ 1,  1], [ 1,  0], [ 1, -1], [ 0,  1], [ 0,  0], [ 0, -1], [-1,  1], [-1,  0], [-1, -1] ])  # Lattice velocities
t = np.array([ 1/float(36), 1/float(9), 1/float(36), 1/float(9), 4/float(9), 1/float(9), 1/float(36), 1/float(9), 1/float(36)])    # Compensation for different lengths of v_i

fin = np.zeros((9, nx, ny))               # Inlet population
fout = np.zeros((9, nx, ny))              # Outlet population

# Initial perturbation
def inivel(d, x, y):
    return (1-d) * uL * (1 + 1e-4*np.sin(y/h*2*np.pi))


ini_vel = np.fromfunction(inivel, (2,nx,ny))   # Initial velocity

for i in range(9):
    cu = 3 * (v[i,0]*ini_vel[0,:,:] + v[i,1]*ini_vel[1,:,:])
    fin[i,:,:] = 1*t[i] * (1 + cu + 0.5*cu**2 - (3/float(2) * (ini_vel[0]**2 + ini_vel[1]**2)))

# For every time iteration
for nt in range(t_iter):
    rho = np.zeros((nx, ny))  # Particle density
    for ix in range(nx):
        for iy in range(ny):
            rho[ix, iy] = 0
            for i in range(9):
                rho[ix, iy] += fin[i, ix, iy]

    u = np.zeros((2, nx, ny))  # Lattice velocities
    for ix in range(nx):
        for iy in range(ny):
            u[0, ix, iy] = 0
            u[1, ix, iy] = 0
            for i in range(9):
                u[0, ix, iy] = u[0, ix, iy] + v[i, 0] * fin[i, ix, iy]
                u[1, ix, iy] = u[0, ix, iy] + v[i, 1] * fin[i, ix, iy]

            u[0, ix, iy] = u[0, ix, iy] / float(rho[ix, iy])
            u[1, ix, iy] = u[1, ix, iy] / float(rho[ix, iy])

    # Collision steps
    eq = np.zeros((9, nx, ny))
    for i in range(9):
        vu = 3 * (v[i, 0] * u[0, :, :] + v[i, 1] * u[1, :, :])
        eq[i, :, :] = rho * t[i] * (1 + vu + 0.5 * vu ** 2 - (3 / float(2) * (u[0] ** 2 + u[1] ** 2)))

    fout = fin - omega * (fin - eq)

    # Streaming steps
    for ix in range(nx):
        for iy in range(ny):
            for i in range(9):
                next_x = ix + v[i, 0]
                if next_x < 0:          # Condition if the flow goes beyond x = 0 boundary
                    next_x = nx - 1
                if next_x >= nx:        # Condition if the flow goes beyond x = nx boundary
                    next_x = 0

                next_y = iy + v[i, 1]
                if next_y < 0:          # Condition if the flow goes beyond y = 0 boundary
                    next_y = ny - 1
                if next_y >= ny:        # Condition if the flow goes beyond y = ny boundary
                    next_y = 0

                fin[i, next_x, next_y] = fout[i, ix, iy]    # Flow entering the next node comes out the current node

    # Bounce back boundary conditions
    for i in range(9):
        fout[i, obstacle] = fin[8 - i, obstacle]

    # Outflow conditions:
    fin[col3, -1, :] = fin[col3, -2, :]

    # Inflow conditions:
    rho[0, :] = 1 / (float(1) - u[0, 0, :]) * (np.sum(fin[col2, 0, :], axis=0) + 2 * np.sum(fin[col3, 0, :], axis=0))

    fin[[0, 1, 2], 0, :] = eq[[0, 1, 2], 0, :] + fin[[8, 7, 6], 0, :] - eq[[8, 7, 6], 0, :]

    # Saving plotted flow
    if (nt % 5 == 0):
        plt.clf()
        line1 = plt.imshow(np.sqrt(u[0] ** 2 + u[1] ** 2).transpose(), cmap=cm.Reds)
        plt.savefig("vel.{0:04f}.png".format(nt/5))