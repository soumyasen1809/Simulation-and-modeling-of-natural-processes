# Coursera - Simulation and modeling of natural processes - Cellular Automata

# Importing libraries
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Defining parameters
board = np.zeros((16,16))                       # Defining a 16x16 board
board[2,5] = 1                                  # Board with 1 = Blue and 0 is White

position_old = (4,5)                            # Starting position of the ant - Board position (4,5)
direction_old = (int(np.cos(np.pi/2)), int(np.sin(np.pi/2)))    # Initial direction of movement of the ant - right

fig, ax = plt.subplots()
line1 = ax.matshow(board, cmap=plt.cm.Blues)    # Plotting the board

for i in xrange(16):
    for j in xrange(16):
        c = board[i,j]
        ax.text(i, j, str(c), va='center', ha='center')

plt.ion()
plt.show()


# Movement of the ant
for moves in range(0, 100):
    new_pos_x = position_old[0] + direction_old[0]
    new_pos_y = position_old[1] + direction_old[1]
    position_new = (new_pos_x, new_pos_y)           # New location of the ant when it moves 1 unit

    if board[position_old[0], position_old[1]] == 1:
        direction_old = (int(np.cos((moves + 1) * np.pi / 2)), int(np.sin((moves + 1) * np.pi / 2)))  # Direction of ant
        board[position_old[0], position_old[1]] = 0     # Change colour of the board
    else:
        direction_old = (int(np.cos((moves - 1) * np.pi / 2)), int(np.sin((moves - 1) * np.pi / 2)))  # Direction of ant
        board[position_old[0], position_old[1]] = 1     # Change colour of the board

    position_old = position_new
    # direction_old = (int(np.cos((moves+1)*np.pi / 2)), int(np.sin((moves+1)*np.pi / 2)))
    line1 = ax.matshow(board, cmap=plt.cm.Blues)
    plt.gcf().canvas.draw()                             # Updating the matrix plot


print ("Final board is: ", board)                       # After all moves, final color of the board
