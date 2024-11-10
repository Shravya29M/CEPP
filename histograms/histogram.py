from PIL import Image
import numpy as np
from math import log10, sqrt
import cv2
from skimage.metrics import structural_similarity as compare_ssim

# Calculate Mean Squared Error (MSE)
def calculate_mse(original_image, stego_image):
    original = np.array(Image.open(original_image))
    stego = np.array(Image.open(stego_image))

    mse = np.mean((original - stego) ** 2)
    return mse

# Calculate Peak Signal-to-Noise Ratio (PSNR)
def calculate_psnr(mse, max_pixel=255.0):
    if mse == 0:  # Means the images are identical
        return float('inf')
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

# Calculate Structural Similarity Index (SSIM)
def calculate_ssim(original_image, stego_image):
    original = cv2.imread(original_image)
    stego = cv2.imread(stego_image)

    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    stego_gray = cv2.cvtColor(stego, cv2.COLOR_BGR2GRAY)

    (ssim_value, _) = compare_ssim(original_gray, stego_gray, full=True)
    return ssim_value

# Calculate Payload Capacity (in bits)
def calculate_payload_capacity(original_image):
    image = Image.open(original_image)
    width, height = image.size

    # Assuming you're hiding 1 bit in the least significant bit of each pixel's first channel
    # You can hide 1 bit in each pixel of the red channel (3 channels RGB)
    payload_capacity = width * height * 1  # 1 bit per pixel
    return payload_capacity

# Example usage
if __name__ == "__main__":
    original_image = "input.jpg"
    stego_image = "hidden_message.png"  # After hiding the message
    
    # Calculate metrics
    mse = calculate_mse(original_image, stego_image)
    psnr = calculate_psnr(mse)
    ssim = calculate_ssim(original_image, stego_image)
    payload_capacity = calculate_payload_capacity(stego_image)

    print(f"MSE: {mse}")
    print(f"PSNR: {psnr} dB")
    print(f"SSIM: {ssim}")
    print(f"Payload Capacity: {payload_capacity} bits")