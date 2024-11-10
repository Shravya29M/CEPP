from PIL import Image
import numpy as np
from sklearn.metrics import mean_squared_error

# Load two images
image1 = Image.open('input.jpg').convert('L')  # Convert to grayscale
image2 = Image.open('hidden_message.png').convert('L')  # Convert to grayscale

# Convert images to numpy arrays
image1_array = np.array(image1)
image2_array = np.array(image2)

# Ensure that both images have the same dimensions
if image1_array.shape != image2_array.shape:
    raise ValueError("Images must have the same dimensions for MSE calculation.")

# Flatten the arrays to 1D
image1_flat = image1_array.flatten()
image2_flat = image2_array.flatten()

# Calculate MSE
mse = mean_squared_error(image1_flat, image2_flat)

print("Mean Squared Error between the images:", mse)
