# Coursera - Simulation and modeling of natural processes - Particles and point-like object

# Importing libraries
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import copy

# Defining a class Node
class Node:
    def __init__(self, m, x, y):    # Defining a body
        self.mass = m               # Mass of the body
        self.mass_pos = m*np.array([x,y])   # Mass*Position value stored
        self.momentum = np.array([0,0])
        self.child = None           # No child node

    def add_next_quad(self):
        self.s = 0.5*self.s         # s is the side length of the current quadrant
        return self._subdivide(1) + 2*self._subdivide(0)

    def _subdivide(self, i):
        self.relpos[i] = self.relpos[i] * 2.0
        if self.relpos[i] < 1.0:
            quadrant = 0
        else:
            quadrant = 1
            self.relpos[i] -= 1.0
        return quadrant

    def position(self):
        return self.mass_pos/float(self.mass)

    def dist_nodes(self, other):
        return np.linalg.norm(other.position() - self.position())

    def force_node(self, other):
        d = self.dist_nodes(other)
        return (self.position() - other.position())*(self.mass * other.mass / float(d**3))

    def reset_zero(self):
        self.s = 1
        self.relpos = self.position().copy()


def add_body(body, node):
    new_node = body if node is None else None

    if node is not None and node.s > np.exp(-4):
        if node.child is None:
            new_node = copy.deepcopy(node)
            new_node.child = [None for i in range(4)]
            quadrant = node.add_next_quad()
            new_node.child[quadrant] = node
        else:
            new_node = node

        new_node.mass = new_node.mass + body.mass
        new_node.mass_pos = new_node.mass_pos + body.new_node.mass_pos
        quadrant = body.add_next_quad()
        new_node.child[quadrant] = add_body(body, new_node.child[quadrant])

    return new_node


def force(body, node, theta):
    if node.child is None:
        return node.force_node(body)

    if node.s < node.dist_nodes(body) * theta:
        return node.force_node(body)

    return np.sum(force(body, c, theta) for c in node.child if c is not None)


def verlet(bodies, root, theta, G, dt):
    for body in bodies:
        F = G * force(body, root, theta)
        body.momentum = body.momentum + dt*F
        body.mass_pos = body.mass_pos + dt*body.momentum


# Defining parameters
theta = 0.5
mass = 1.0
ini_radius = 0.1
ini_vel = 0.1
G = 4*np.exp(-6)
dt = 0.001
num_bodies = 10
max_iter = 10
f_samp = 2

np.random.seed(1)
pos_x = np.random.random(num_bodies) *2.0*ini_radius + 0.5-ini_radius
pos_y = np.random.random(num_bodies) *2.0*ini_radius + 0.5-ini_radius
bodies = [ Node(mass, px, py) for (px,py) in zip(pos_x, pos_y) if (px-0.5)**2 + (py-0.5)**2 < ini_radius**2 ]
for body in bodies:
    r = body.position() - np.array([0.5,0.5])
    body.momentum = np.array([-r[1], -r[0]]) * mass * ini_vel * np.linalg.norm(r)/float(ini_radius)

# Time iteration
for i in range(max_iter):
    root = None
    for body in bodies:
        body.reset_zero()
        root = add_body(body, root)

    verlet(bodies, root, theta, G, dt)

    if i % f_samp == 0:
        print("Writing images at iteration {0}".format(i))
        ax = plt.gcf().add_subplot(111, aspect='equal')
        ax.cla()
        ax.scatter([b.position()[0] for b in bodies], [b.position()[1] for b in bodies], 1)
        ax.set_xlim([0., 1.0])
        ax.set_ylim([0., 1.0])
        plt.gcf().savefig('bodies_{0:06}.png'.format(i/f_samp))

