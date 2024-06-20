import numpy as np

# Format: [azimuth, elevation] (in radians)
# Azimuth: 0 = front; pi/2 = left; pi = rear; 1.5pi = right
# Elevation: 0 = horizontal; pi/2 = zenith; -pi/2 = nadir

# Define the directions of the speakers for the VCCM array
speakers = [
    [1 * np.pi / 4, 0],  # speaker #1 (left front bottom)
    [0 * np.pi / 4, 0],  # speaker #2 (center bottom)
    [7 * np.pi / 4, 0],
    [6 * np.pi / 4, 0],
    [5 * np.pi / 4, 0],
    [4 * np.pi / 4, 0],
    [3 * np.pi / 4, 0],
    [2 * np.pi / 4, 0],
    [(1 * np.pi / 4) - (np.pi / 8), np.pi / 4],  # speaker #9 (left front top)
    [(0 * np.pi / 4) - (np.pi / 8), np.pi / 4],  # speaker #10 (right front)
    [(7 * np.pi / 4) - (np.pi / 8), np.pi / 4],
    [(6 * np.pi / 4) - (np.pi / 8), np.pi / 4],
    [(5 * np.pi / 4) - (np.pi / 8), np.pi / 4],
    [(4 * np.pi / 4) - (np.pi / 8), np.pi / 4],
    [(3 * np.pi / 4) - (np.pi / 8), np.pi / 4],
    [(2 * np.pi / 4) - (np.pi / 8), np.pi / 4]
]

# Define functions to calculate components of speaker directions
def w_i(azi, ele):
    return 1

def y_i(azi, ele):
    return np.sqrt(3) * np.cos(ele) * np.sin(azi)

def z_i(azi, ele):
    return np.sqrt(3) * np.sin(ele)

def x_i(azi, ele):
    return np.sqrt(3) * np.cos(azi) * np.cos(ele)

# Functions for 2nd order components
def v_i(azi, ele):
    return (np.sqrt(15) / 2) * np.cos(ele)**2 * np.sin(2 * azi)

def t_i(azi, ele):
    return (np.sqrt(15) / 2) * np.sin(2 * ele) * np.sin(azi)

def r_i(azi, ele):
    return (np.sqrt(5) / 2) * (3 * np.sin(ele)**2 - 1)

def s_i(azi, ele):
    return (np.sqrt(15) / 2) * np.sin(2 * ele) * np.cos(azi)

def u_i(azi, ele):
    return (np.sqrt(15) / 2) * np.cos(ele)**2 * np.cos(2 * azi)

# Calculate coefficients for 1st and 2nd order ambisonics
K = []
for l in speakers:
    K.append([
        w_i(l[0], l[1]), x_i(l[0], l[1]), y_i(l[0], l[1]), z_i(l[0], l[1]),
        v_i(l[0], l[1]), t_i(l[0], l[1]), r_i(l[0], l[1]), s_i(l[0], l[1]), u_i(l[0], l[1])
    ])

# Find pseudo-inverse matrix
K = np.matrix(K)
M = (np.linalg.pinv(K)).T.round(7)

# Write the pseudo-inverse matrix to a file
with open("VCCM.txt", "w") as file:
    for row in M:
        for element in row:
            file.write(f"{element};\n")
