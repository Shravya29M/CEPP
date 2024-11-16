# Secure Data Embedding: Caesar, AES, and Multi-Layer Steganographic Methods

This repository contains the implementation of secure data embedding techniques using **Center-Embedded Pixel Positioning (CEPP)**. The methods incorporate **Caesar Cipher**, **AES Encryption**, and **Multi-Layer Steganography** to enhance the security and integrity of hidden information within digital images.

## Overview

This project explores the following key methods for secure data embedding:
- **Caesar Cipher**: A basic encryption technique that shifts characters in the plaintext by a specified number of positions.
- **AES Encryption**: A robust cryptographic standard ensuring secure data protection.
- **Multi-Layer Steganography**: A combination of embedding techniques using multiple color channels for enhanced security.

The repository also includes an evaluation framework to assess these techniques using metrics such as **MSE**, **PSNR**, and **SSIM**.

## Project Structure

The repository is divided into the following key files:

1. **`aes.py`**  
   Implements CEPP with AES Encryption.  
   - Encrypts data using AES.
   - Embeds binary data into the least significant bits (LSBs) of image pixels.  

2. **`caesar.py`**  
   Implements CEPP with Caesar Cipher.  
   - Encrypts text using the Caesar Cipher algorithm.
   - Embeds the encrypted text in the LSBs of image pixels.  

3. **`multi_layer_steganography.py`**  
   Implements CEPP with Multi-Layer Steganography.  
   - Utilizes multiple color channels (Red and Green) for embedding.
   - Follows a spiral pattern for secure data embedding.

4. **`model_evaluation.py`**  
   Evaluates the performance of the above methods using metrics:
   - **Mean Squared Error (MSE)**
   - **Peak Signal-to-Noise Ratio (PSNR)**
   - **Structural Similarity Index (SSIM)**
   - **Entropy**

## Results

The techniques demonstrate minimal alteration to image quality while providing strong data concealment. Detailed evaluations are available in the **Results** section of the research paper.

| Method                  | MSE             | PSNR (dB)       | SSIM           | Payload Capacity (bits) |
|-------------------------|-----------------|-----------------|----------------|-------------------------|
| **Caesar Cipher**       | `1.0579e-05`   | `97.886`        | `0.9999999901` | `7,372,800`            |
| **AES Encryption**      | `0.00010959`   | `87.733`        | `0.9999997193` | `7,372,800`            |
| **Multi-Layer Steganography** | `0.00010634` | `87.864`        | `0.9999999441` | `7,372,800`            |

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/secure-data-embedding.git
   cd secure-data-embedding
