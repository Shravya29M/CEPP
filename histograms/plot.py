import numpy as np
import matplotlib.pyplot as plt

# Data
methods = ['CEPP with Caesar', 'CEPP with AES', 'CEPP with Multi-layer']

mse_values = [5.477184864691625e-07, 1.0510978573670119e-05, 1.0458814908292104e-05]
psnr_values = [110.74522961483665, 97.91437210076474, 97.935978835974]
ssim_values = [0.9999999996814569, 0.9999999868668085, 0.9999999764045074]
payload_capacity = [12780288, 12780288, 12780288]  # Constant for all methods

# Create subplots for MSE, PSNR, SSIM, and Payload
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# MSE plot
axs[0, 0].bar(methods, mse_values, color='skyblue')
axs[0, 0].set_title('MSE')
axs[0, 0].set_ylabel('MSE (log scale)')
axs[0, 0].set_yscale('log')  # Log scale for better visualization of small values

# PSNR plot
axs[0, 1].bar(methods, psnr_values, color='lightgreen')
axs[0, 1].set_title('PSNR (dB)')
axs[0, 1].set_ylabel('PSNR (dB)')

# SSIM plot
axs[1, 0].bar(methods, ssim_values, color='lightcoral')
axs[1, 0].set_title('SSIM')
axs[1, 0].set_ylabel('SSIM')

# Payload Capacity plot
axs[1, 1].bar(methods, payload_capacity, color='gold')
axs[1, 1].set_title('Payload Capacity')
axs[1, 1].set_ylabel('Payload (bits)')

# Adjust layout and display
plt.tight_layout()
plt.show()
