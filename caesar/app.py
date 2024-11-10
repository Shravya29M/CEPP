from PIL import Image
import bitarray

def caesar_cipher_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_cipher_decrypt(encrypted_text, shift):
    return caesar_cipher_encrypt(encrypted_text, -shift)

def hide_message(image_path, message, shift):
    # Encrypt the message using Caesar cipher
    encrypted_message = caesar_cipher_encrypt(message, shift)
    
    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Convert the message to binary
    ba = bitarray.bitarray()
    ba.frombytes(encrypted_message.encode('utf-8'))
    binary_message = ba.to01()

    # Calculate the starting position for hiding the message
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

    # Save the modified image
    image.save('hidden_message.png')

def retrieve_message(image_path, message_length, shift):
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
            if index < message_length * 8:
                pixel = list(image.getpixel((x, y)))
                binary_message += str(pixel[0] & 1)
                index += 1
            else:
                break

    # Convert the binary message to text
    ba = bitarray.bitarray(binary_message)
    encrypted_message = ba.tobytes().decode('utf-8')

    # Decrypt the message using Caesar cipher
    decrypted_message = caesar_cipher_decrypt(encrypted_message, shift)
    
    return encrypted_message, decrypted_message

# Hide or retrieve a message in/from an image

print("1. Hide Message")
print("2. Retrieve Message")

# Function to save the value of shift to a file
def save_shift(shift):
    with open("shift.txt", "w") as file:
        file.write(str(shift))

# Function to read the value of shift from a file
def load_shift():
    try:
        with open("shift.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return None

# Load the value of shift from the file
shift = load_shift()

choice = int(input("Enter a choice: "))
# Function to save the length of the original message to a file
def save_message_length(length):
    with open("message_length.txt", "w") as file:
        file.write(str(length))

# Function to read the length of the original message from a file
def load_message_length():
    try:
        with open("message_length.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return None

if choice == 1:
    mess = input("Enter the message: ")
    mess_length = len(mess)
    save_message_length(mess_length)  # Save the length of the original message
    shift = int(input("Enter the Caesar cipher shift (key): "))
    save_shift(shift)  # Save the value of shift to a file
    fname = input("Enter the filename or path of the image file: ")
    hide_message(fname, mess, shift)
    print("Message hidden successfully!")
elif choice == 2:
    if shift is None:
        print("Invalid choice. You must choose option 1 first.")
    else:
        fname = input("Enter the filename or path of the image file: ")
        length = int(input("Enter the length of the hidden message: "))
        shift_1 = int(input("Enter the Caesar cipher shift used for encryption: "))
        encrypted_message, decrypted_message = retrieve_message(fname, length, shift_1)
        if encrypted_message is not None and decrypted_message is not None:
            original_length = load_message_length()  # Load the length of the original message
            if original_length is not None and original_length == length and shift == shift_1:
                print("Encrypted message:", encrypted_message)
                decrypt_key = int(input("Enter the Caesar cipher shift (key) to decrypt the message: "))
                if decrypt_key == shift_1 and decrypt_key == shift:
                    print("Decrypted message:", decrypted_message)
                else:
                    print("Invalid Caesar cipher key! Unable to decrypt the message.")
            else:
                print("Invalid key used!")
        else:
            print("Unable to retrieve the message.")
else:
    print("Invalid choice")
