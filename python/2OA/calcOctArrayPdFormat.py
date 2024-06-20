import numpy as np

# Format: [azimuth, elevation] (in radians)
# Azimuth: 0 = front; pi/2 = left; pi = rear; 1.5pi = right
# Elevation: 0 = horizontal; pi/2 = zenith; -pi/2 = nadir

# Define the directions of the speakers for the octagonal array
speakers = [
    [(0 * np.pi / 4) + (np.pi / 8), 0],  # speaker 1, Left
    [(7 * np.pi / 4) + (np.pi / 8), 0],  # speaker 2, Right
    [(6 * np.pi / 4) + (np.pi / 8), 0],
    [(5 * np.pi / 4) + (np.pi / 8), 0],
    [(4 * np.pi / 4) + (np.pi / 8), 0],
    [(3 * np.pi / 4) + (np.pi / 8), 0],
    [(2 * np.pi / 4) + (np.pi / 8), 0],
    [(1 * np.pi / 4) + (np.pi / 8), 0]
]

# Define functions to calculate components of speaker directions according to N3D convention
def w_i(azi, ele):
    return 1

def y_i(azi, ele):
    return np.sqrt(3) * np.cos(azi) * np.sin(ele)

def z_i(azi, ele):
    return np.sqrt(3) * np.sin(azi)

def x_i(azi, ele):
    return np.sqrt(3) * np.cos(azi) * np.cos(ele)

# Functions for 2nd order components
def v_i(azi, ele):
    return (np.sqrt(15) / 2) * np.cos(azi)**2 * np.sin(2 * ele)

def t_i(azi, ele):
    return (np.sqrt(15) / 2) * np.sin(2 * azi) * np.sin(ele)

def r_i(azi, ele):
    return (np.sqrt(5) / 2) * (3 * np.sin(ele)**2 - 1)

def s_i(azi, ele):
    return (np.sqrt(15) / 2) * np.sin(2 * azi) * np.cos(ele)

def u_i(azi, ele):
    return (np.sqrt(15) / 2) * np.cos(azi)**2 * np.cos(2 * ele)

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
with open("Oct.txt", "w") as file:
    for row in M:
        for element in row:
            file.write(f"{element};\n")
