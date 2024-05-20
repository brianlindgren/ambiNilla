import numpy as np

# Format: [azimuth, elevation] (in radians)
# Azimuth: 0 = front; pi/2 = left; pi = rear; 1.5pi = right
# Elevation: 0 = horizontal; pi/2 = zenith; -pi/2 = nadir

# For details, see "Is My Decoder Ambisonic?", Heller, Lee, and Benjamin, 2008.

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
def x_i(azi, ele):
    return np.cos(azi) * np.cos(ele)

def y_i(azi, ele):
    return np.sin(azi) * np.cos(ele)

def z_i(azi, ele):
    return np.sin(ele)

def w_i(azi, ele):
    return np.sqrt(2) / 2

# Calculate coefficients
K = []
for l in speakers:
    K.append([w_i(l[0], l[1]), x_i(l[0], l[1]), y_i(l[0], l[1]), z_i(l[0], l[1])])

# Find pseudo-inverse matrix
K = np.matrix(K).round(4)
M = (np.linalg.pinv(K)).T.round(4)

# Write the pseudo-inverse matrix to a file
with open("output.txt", "w") as file:
    for row in M:
        for element in row:
            file.write(f"{element};\n")
