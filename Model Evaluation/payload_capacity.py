from PIL import Image
import numpy as np

def calculate_payload_capacity(image_path, hidden_data_size_bytes):

    # Load the cover image
    image = Image.open("input.jpg")
    
    # Get image dimensions (width and height)
    width, height = image.size
    
    # Total number of pixels in the image
    total_pixels = width * height
    
    # Convert hidden data size to bits (1 byte = 8 bits)
    hidden_data_size_bits = hidden_data_size_bytes * 8
    
    # Calculate payload capacity (bits per pixel)
    payload_capacity_bpp = hidden_data_size_bits / total_pixels
    
    return payload_capacity_bpp

# Example usage
image_path = 'input.img'  # Replace with your image path
hidden_message = "Hello!"
hidden_data_size_bytes = len(hidden_message.encode('utf-8'))


# Calculate payload capacity
capacity_bpp = calculate_payload_capacity("input.jpg", hidden_data_size_bytes)

print(f"Payload Capacity: {capacity_bpp:.4f} bits per pixel (bpp)")
