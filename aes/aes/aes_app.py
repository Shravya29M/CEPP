from PIL import Image
import bitarray
from cryptography.fernet import Fernet

# Encrypt function using Fernet (AES encryption)
def aes_encrypt(message):
    key = load_key()  # Load the key for encryption
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode('utf-8'))
    return encrypted_message

# Decrypt function using Fernet (AES decryption)
def aes_decrypt(encrypted_message):
    key = load_key()  # Load the key for decryption
    fernet = Fernet(key)
    try:
        decrypted_message = fernet.decrypt(encrypted_message).decode('utf-8')
        return decrypted_message
    except cryptography.fernet.InvalidToken:
        print("Decryption failed. Invalid token or altered message.")
        return None

# Generate key (one-time operation)
def generate_key():
    key = Fernet.generate_key()
    with open('encryption_key.key', 'wb') as key_file:
        key_file.write(key)

# Load key for encryption/decryption
def load_key():
    with open('encryption_key.key', 'rb') as key_file:
        return key_file.read()

# Hide the encrypted message in the image
def hide_message(image_path, message):
    encrypted_message = aes_encrypt(message)  # Encrypt the message
    
    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Convert the encrypted message to binary
    ba = bitarray.bitarray()
    ba.frombytes(encrypted_message)
    binary_message = ba.to01()

    # Calculate the starting position for hiding the message (Center Embedded Pixel Positioning)
    start_x = width // 2
    start_y = height // 2

    # Hide the message in the image
    index = 0
    for y in range(start_y, height):
        for x in range(start_x, width):
            if index < len(binary_message):
                pixel = list(image.getpixel((x, y)))
                pixel[0] = pixel[0] & ~1 | int(binary_message[index])
                image.putpixel((x, y), tuple(pixel))
                index += 1
            else:
                break

    # Save the modified image with the hidden message
    image.save('hidden_message_aes.png')
    print("Message hidden successfully!")

# Retrieve the encrypted message from the image
def retrieve_message(image_path):
    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the starting position for retrieving the message
    start_x = width // 2
    start_y = height // 2

    # Retrieve the message from the image
    binary_message = ''
    for y in range(start_y, height):
        for x in range(start_x, width):
            pixel = list(image.getpixel((x, y)))
            binary_message += str(pixel[0] & 1)

    # Convert the binary message back to bytes
    ba = bitarray.bitarray(binary_message)
    encrypted_message = ba.tobytes()

    # Decrypt the message using Fernet (AES decryption)
    decrypted_message = aes_decrypt(encrypted_message)
    
    if decrypted_message:
        print("Decrypted message:", decrypted_message)
        return decrypted_message
    else:
        print("Failed to retrieve the message.")
        return None

# Main script
print("1. Hide Message")
print("2. Retrieve Message")

# Ensure the encryption key exists
try:
    load_key()
except FileNotFoundError:
    generate_key()

choice = int(input("Enter a choice: "))

if choice == 1:
    # Hide a message
    message = input("Enter the message: ")
    image_file = input("Enter the filename or path of the image file: ")
    hide_message(image_file, message)

elif choice == 2:
    # Retrieve a message
    image_file = input("Enter the filename or path of the image file: ")
    retrieved_message = retrieve_message(image_file)
    
else:
    print("Invalid choice")
