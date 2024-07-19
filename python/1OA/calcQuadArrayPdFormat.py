import numpy as np

# Format: [azimuth, elevation] (in radians)
# Azimuth: 0 = front; pi/2 = left; pi = rear; 1.5pi = right
# Elevation: 0 = horizontal; pi/2 = zenith; -pi/2 = nadir

# Quad speaker array:
speakers = [
    [np.pi / 4, 0],  # front left
    [7 * np.pi / 4, 0],  # front right
    [5 * np.pi / 4, 0],  # rear right
    [3 * np.pi / 4, 0]   # rear left
]

# Define functions to calculate components of speaker directions according to N3D convention
def w_i(azi, ele):
    return 1

def y_i(azi, ele):
    return np.sqrt(3) * np.cos(ele) * np.sin(azi)

def z_i(azi, ele):
    return np.sqrt(3) * np.sin(ele)

def x_i(azi, ele):
    return np.sqrt(3) * np.cos(azi) * np.cos(ele)

# Calculate coefficients
K = []
for l in speakers:
    K.append([w_i(l[0], l[1]), x_i(l[0], l[1]), y_i(l[0], l[1]), z_i(l[0], l[1])])

# Find pseudo-inverse matrix
K = np.matrix(K)
M = (np.linalg.pinv(K)).T.round(7)

# Write the pseudo-inverse matrix to a file
with open("Quad.txt", "w") as file:
    for row in M:
        for element in row:
            file.write(f"{element};\n")
