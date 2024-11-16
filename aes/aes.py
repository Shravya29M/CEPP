from PIL import Image
import bitarray
from cryptography.fernet import Fernet, InvalidToken

def aes_encrypt(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode('utf-8'))
    return encrypted_message

def aes_decrypt(encrypted_message, key):
    fernet = Fernet(key)
    try:
        decrypted_message = fernet.decrypt(encrypted_message).decode('utf-8')
    except InvalidToken:
        print("Error: The token is invalid or the decryption key is incorrect.")
        decrypted_message = None
    return decrypted_message

def hide_message(image_path, message, key):
    encrypted_message = aes_encrypt(message, key)
    
    # Convert the message to binary
    ba = bitarray.bitarray()
    ba.frombytes(encrypted_message)
    binary_message = ba.to01()

    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the starting position for hiding the message
    start_x = width // 2
    start_y = height // 2

    # Ensure the image has enough capacity
    if len(binary_message) > (width - start_x) * (height - start_y):
        raise ValueError("The image is too small to hide the entire message.")

    # Hide the message in the image
    index = 0
    for y in range(start_y, height):
        for x in range(start_x, width):
            if index < len(binary_message):
                pixel = list(image.getpixel((x, y)))
                pixel[0] = (pixel[0] & ~1) | int(binary_message[index])
                image.putpixel((x, y), tuple(pixel))
                index += 1
            else:
                break
        if index >= len(binary_message):
            break

    # Save the modified image
    image.save('multi_layer_hidden_message.png')
    print("Message hidden successfully!")

def retrieve_message(image_path, binary_message_length, key):
    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the starting position for retrieving the message
    start_x = width // 2
    start_y = height // 2

    # Retrieve the message from the image
    binary_message = ''
    index = 0
    for y in range(start_y, height):
        for x in range(start_x, width):
            if index < binary_message_length:
                pixel = list(image.getpixel((x, y)))
                binary_message += str(pixel[0] & 1)
                index += 1
            else:
                break
        if index >= binary_message_length:
            break

    # Check if binary_message length is a multiple of 8 and pad if necessary
    if len(binary_message) % 8 != 0:
        binary_message = binary_message.ljust(len(binary_message) + (8 - len(binary_message) % 8), '0')

    # Convert the binary message to bytes
    ba = bitarray.bitarray(binary_message)
    encrypted_message = ba.tobytes()
    
    decrypted_message = aes_decrypt(encrypted_message, key)
    
    return encrypted_message, decrypted_message

def main():
    choice = input("Do you want to (1) hide a message or (2) retrieve a message? Enter 1 or 2: ")
    
    if choice == '1':
        image_path = input("Enter the path to the image file: ")
        message = input("Enter the message to hide: ")
        key = Fernet.generate_key()
        print("Encryption Key:", key.decode())
        hide_message(image_path, message, key)
        
    elif choice == '2':
        image_path = input("Enter the path to the image file: ")
        key = input("Enter the encryption key: ").encode()
        encrypted_message_length = len(aes_encrypt('', key))
        encrypted_message, decrypted_message = retrieve_message(image_path, encrypted_message_length * 8, key)
        print("Decrypted Message:", decrypted_message)
        
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
