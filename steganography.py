from PIL import Image

def encode_message(image_path, message, output_path):
    # Open the original image
    org_img = Image.open(image_path)
    org_pixelMap = org_img.load()

    # Create a new image object with the same mode and size as the original image
    enc_img = Image.new(org_img.mode, org_img.size)
    enc_pixelsMap = enc_img.load()

    msg_len = len(message)
    msg_index = 0

    # Traverse through the pixels of the original image
    for row in range(org_img.size[0]):
        for col in range(org_img.size[1]):
            r, g, b = org_pixelMap[row, col]

            if row == 0 and col == 0:
                # Store the length of the message in the first pixel
                enc_pixelsMap[row, col] = (msg_len, g, b)
            elif msg_index < msg_len:
                # Hide the message in the R value of the pixels
                ascii_value = ord(message[msg_index])
                enc_pixelsMap[row, col] = (ascii_value, g, b)
                msg_index += 1
            else:
                # Copy the original pixel values if the message is fully encoded
                enc_pixelsMap[row, col] = (r, g, b)

    # Save the encoded image
    enc_img.save(output_path)
    enc_img.show()
    org_img.close()
    enc_img.close()
    print(f"Message has been encoded into '{output_path}'.")

def decode_message(image_path):
    # Open the encoded image
    enc_img = Image.open(image_path)
    enc_pixelMap = enc_img.load()

    # Get the length of the message from the first pixel
    msg_len = enc_pixelMap[0, 0][0]
    decoded_message = ""

    msg_index = 0

    # Traverse through the pixels to decode the message
    for row in range(enc_img.size[0]):
        for col in range(enc_img.size[1]):
            if msg_index < msg_len:
                r, g, b = enc_pixelMap[row, col]
                decoded_message += chr(r)
                msg_index += 1
            else:
                break
        if msg_index >= msg_len:
            break

    enc_img.close()
    print("The hidden message is:\n\n" + decoded_message)

def main():
    choice = input("Do you want to (e)ncode or (d)ecode a message? Enter 'e' or 'd': ").lower()
    image_path = input("Enter the path to the image: ")

    if choice == 'e':
        secret_message = input("Enter the secret message: ")
        output_path = "encrypted_image.png"
        encode_message(image_path, secret_message, output_path)
    elif choice == 'd':
        decode_message(image_path)
    else:
        print("Invalid choice. Please enter 'e' to encode or 'd' to decode.")

if __name__ == "__main__":
    main()

