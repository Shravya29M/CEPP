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

def hide_messages(image_path, messages, key):
    encrypted_messages = [aes_encrypt(msg, key) for msg in messages]
    binary_messages = [bitarray.bitarray() for _ in encrypted_messages]
    
    for i, encrypted_message in enumerate(encrypted_messages):
        ba = bitarray.bitarray()
        ba.frombytes(encrypted_message)
        binary_messages[i] = ba.to01()

    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the center starting position
    start_x = width // 2
    start_y = height // 2

    # Ensure the image has enough capacity
    total_length = sum(len(bm) for bm in binary_messages)
    num_pixels = (width - start_x) * (height - start_y)
    if total_length > num_pixels * 3:  # 3 channels: R, G, B
        raise ValueError("The image is too small to hide the entire message.")

    # Hide each message starting from the center
    for i in range(len(binary_messages)):
        binary_message = binary_messages[i]
        index = 0
        # Start embedding from the center and work outwards
        for distance in range(max(width, height)):
            for dx in range(-distance, distance + 1):
                for dy in [-distance, distance]:  # top and bottom row for the given distance
                    x = start_x + dx
                    y = start_y + dy
                    if 0 <= x < width and 0 <= y < height and index < len(binary_message):
                        pixel = list(image.getpixel((x, y)))
                        channel = i % 3  # Rotate through R, G, B channels
                        pixel[channel] = (pixel[channel] & ~1) | int(binary_message[index])
                        image.putpixel((x, y), tuple(pixel))
                        index += 1
            for dy in range(-distance + 1, distance):  # left and right columns for the given distance
                x = start_x + distance
                y = start_y + dy
                if 0 <= x < width and 0 <= y < height and index < len(binary_message):
                    pixel = list(image.getpixel((x, y)))
                    channel = i % 3  # Rotate through R, G, B channels
                    pixel[channel] = (pixel[channel] & ~1) | int(binary_message[index])
                    image.putpixel((x, y), tuple(pixel))
                    index += 1

    # Save the modified image
    image.save('multi_layer_hidden_message.png')
    print("Messages hidden successfully!")

def retrieve_messages(image_path, message_lengths, key):
    image = Image.open(image_path)
    width, height = image.size
    start_x = width // 2
    start_y = height // 2

    decrypted_messages = []
    
    for length in message_lengths:
        binary_message = ''
        index = 0
        # Retrieve messages starting from the center
        for distance in range(max(width, height)):
            for dx in range(-distance, distance + 1):
                for dy in [-distance, distance]:  # top and bottom row for the given distance
                    x = start_x + dx
                    y = start_y + dy
                    if 0 <= x < width and 0 <= y < height and index < length:
                        pixel = list(image.getpixel((x, y)))
                        channel = len(decrypted_messages) % 3  # Rotate through R, G, B channels
                        binary_message += str(pixel[channel] & 1)
                        index += 1
            for dy in range(-distance + 1, distance):  # left and right columns for the given distance
                x = start_x + distance
                y = start_y + dy
                if 0 <= x < width and 0 <= y < height and index < length:
                    pixel = list(image.getpixel((x, y)))
                    channel = len(decrypted_messages) % 3  # Rotate through R, G, B channels
                    binary_message += str(pixel[channel] & 1)
                    index += 1

        # Convert the binary message to bytes and decrypt
        ba = bitarray.bitarray(binary_message)
        encrypted_message = ba.tobytes()
        decrypted_message = aes_decrypt(encrypted_message, key)
        decrypted_messages.append(decrypted_message)

    return decrypted_messages

def main():
    choice = input("Do you want to (1) hide messages or (2) retrieve messages? Enter 1 or 2: ")
    
    if choice == '1':
        image_path = input("Enter the path to the image file: ")
        messages = input("Enter the messages to hide (comma separated): ").split(',')
        key = Fernet.generate_key()
        print("Encryption Key:", key.decode())
        hide_messages(image_path, [msg.strip() for msg in messages], key)
        
    elif choice == '2':
        image_path = input("Enter the path to the image file: ")
        key = input("Enter the encryption key: ").encode()
        message_lengths = list(map(int, input("Enter the lengths of the encrypted messages (comma separated): ").split(',')))
        decrypted_messages = retrieve_messages(image_path, message_lengths, key)
        for i, msg in enumerate(decrypted_messages):
            print(f"Decrypted Message {i+1}:", msg)
        
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
