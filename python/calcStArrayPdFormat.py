import numpy as np

# Format: [azimuth, elevation] (in radians)
# Azimuth: 0 = front; pi/2 = left; pi = rear; 1.5pi = right
# Elevation: 0 = horizontal; pi/2 = zenith; -pi/2 = nadir

# For details, see "Is My Decoder Ambisonic?", Heller, Lee, and Benjamin, 2008.

# Define the directions of the speakers for the st at 45 deg L and 45 deg R

speakers = [
    [0.785399, 0],  # left
    [5.497781, 0]  # right
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
