from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np

def calculate_ssim(image1_path, image2_path):

    # Load the images
    image1 = Image.open("input.jpg")
    image2 = Image.open("hidden_message.png")

    # Convert images to grayscale (required for SSIM calculation)
    image1_gray = image1.convert('L')
    image2_gray = image2.convert('L')

    # Convert images to numpy arrays
    image1_array = np.array(image1_gray)
    image2_array = np.array(image2_gray)

    # Calculate SSIM between the two images
    ssim_value, _ = ssim(image1_array, image2_array, full=True)
    
    return ssim_value

# Example usage
image1_path = 'input.jpg'  # Replace with your image path
image2_path = 'hidden_message.png'     # Replace with your image path

# Calculate SSIM
ssim_value = calculate_ssim(image1_path, image2_path)

print(f"SSIM: {ssim_value:.4f}")
