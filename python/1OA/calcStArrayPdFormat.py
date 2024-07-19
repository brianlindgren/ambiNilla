import numpy as np

# Format: [azimuth, elevation] (in radians)
# Azimuth: 0 = front; pi/2 = left; pi = rear; 1.5pi = right
# Elevation: 0 = horizontal; pi/2 = zenith; -pi/2 = nadir

# For details, see "Is My Decoder Ambisonic?", Heller, Lee, and Benjamin, 2008.

# Define the directions of the speakers for the st at 45 deg L and 45 deg R
speakers = [
    [np.pi / 4, 0],   # left (45 degrees)
    [7 * np.pi / 4, 0]  # right (315 degrees, equivalent to -45 degrees)
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

# Calculate coefficients
K = []
for l in speakers:
    K.append([w_i(l[0], l[1]), x_i(l[0], l[1]), y_i(l[0], l[1]), z_i(l[0], l[1])])

# Find pseudo-inverse matrix
K = np.matrix(K)
M = (np.linalg.pinv(K)).T.round(7)

# Write the pseudo-inverse matrix to a file
with open("Stereo.txt", "w") as file:
    for row in M:
        for element in row:
            file.write(f"{element};\n")
