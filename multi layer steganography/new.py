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

def hide_multiple_messages(image_path, messages, key):
    encrypted_messages = [aes_encrypt(message, key) for message in messages]
    
    # Convert the messages to binary
    binary_messages = [bitarray.bitarray().frombytes(encrypted_message).to01() for encrypted_message in encrypted_messages]

    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the starting position for hiding the messages
    start_x = width // 2
    start_y = height // 2

    # Ensure the image has enough capacity
    num_pixels = (width - start_x) * (height - start_y)
    total_bits_required = sum(len(bm) for bm in binary_messages)
    
    if total_bits_required > num_pixels * 3:  # 3 channels: R, G, B
        raise ValueError("The image is too small to hide the entire message.")

    # Hide the messages in the image
    index = 0
    for y in range(start_y, height):
        for x in range(start_x, width):
            if index < total_bits_required:
                pixel = list(image.getpixel((x, y)))
                
                for channel in range(3):  # 0: R, 1: G, 2: B
                    if index < total_bits_required:
                        bit_to_hide = 0  # Default to 0
                        for bm in binary_messages:
                            if index < len(bm):
                                bit_to_hide = int(bm[index])
                                index += 1
                                break

                        # Modify the pixel's channel bit
                        pixel[channel] = (pixel[channel] & ~1) | bit_to_hide

                # Update the pixel
                image.putpixel((x, y), tuple(pixel))

            else:
                break
        if index >= total_bits_required:
            break

    # Save the modified image
    image.save('multi_layer_hidden_message.png')
    print("Messages hidden successfully!")

def retrieve_multiple_messages(image_path, message_count, key):
    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the starting position for retrieving the messages
    start_x = width // 2
    start_y = height // 2

    # Prepare to retrieve the binary messages
    binary_messages = ['' for _ in range(message_count)]
    index = 0
    for y in range(start_y, height):
        for x in range(start_x, width):
            if index < message_count * 8 * 3:  # Assuming 8 bits per channel
                pixel = list(image.getpixel((x, y)))
                
                channel_bits = [p & 1 for p in pixel[:3]]  # Get least significant bits of RGB

                for channel in range(3):  # R, G, B channels
                    if index < message_count * 8 * 3:
                        binary_messages[index // 8] += str(channel_bits[channel])
                        index += 1
                    else:
                        break
            else:
                break
        if index >= message_count * 8 * 3:
            break

    decrypted_messages = []
    for binary_message in binary_messages:
        # Pad the binary message to be a multiple of 8
        if len(binary_message) % 8 != 0:
            binary_message = binary_message.ljust(len(binary_message) + (8 - len(binary_message) % 8), '0')
        
        # Convert the binary message to bytes
        ba = bitarray.bitarray(binary_message)
        encrypted_message = ba.tobytes()
        
        decrypted_message = aes_decrypt(encrypted_message, key)
        decrypted_messages.append(decrypted_message)
    
    return decrypted_messages

def main():
    choice = input("Do you want to (1) hide messages or (2) retrieve messages? Enter 1 or 2: ")
    
    if choice == '1':
        image_path = input("Enter the path to the image file: ")
        messages = []
        num_messages = int(input("Enter the number of messages to hide: "))
        for i in range(num_messages):
            message = input(f"Enter message {i + 1} to hide: ")
            messages.append(message)
        key = Fernet.generate_key()
        print("Encryption Key:", key.decode())
        hide_multiple_messages(image_path, messages, key)
        
    elif choice == '2':
        image_path = input("Enter the path to the image file: ")
        key = input("Enter the encryption key: ").encode()
        num_messages = int(input("Enter the number of messages hidden: "))
        decrypted_messages = retrieve_multiple_messages(image_path, num_messages, key)
        for i, msg in enumerate(decrypted_messages):
            print(f"Decrypted Message {i + 1}: {msg}")

    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
