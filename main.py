from PIL import Image


def hide_text(image_path, text, output_path):
    img = Image.open(image_path)
    pixels = img.load()

    text_binary = ''.join(format(ord(char), '08b') for char in text)
    text_length = len(text_binary)

    index = 0

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if index < text_length:
                pixel = list(pixels[i, j])
                for k in range(3):  # Modify the least significant bit of RGB
                    if index < text_length:
                        pixel[k] = pixel[k] & 254 | int(text_binary[index])
                        index += 1
                pixels[i, j] = tuple(pixel)

    img.save(output_path)


def extract_text(image_path, text_length=None):
    img = Image.open(image_path)
    pixels = img.load()

    binary_text = ''
    index = 0

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = list(pixels[i, j])
            for k in range(3):  # Extract the least significant bit of RGB
                binary_text += str(pixel[k] & 1)
                index += 1
                if text_length is not None and index >= text_length * 8:
                    break
            if text_length is not None and index >= text_length * 8:
                break

    if text_length is not None:
        extracted_text = ''
        for i in range(0, len(binary_text), 8):
            byte = binary_text[i:i + 8]
            extracted_text += chr(int(byte, 2))
    else:
        extracted_text = binary_text  # Return all binary data

    return extracted_text





if __name__ == "__main__":
    action = input("What should be done? (hide/find): ")
    if action == "hide":
        input_image_path = input("Enter input image name: ")
        text = input("Enter Text: ")
        output_image_path = input("Enter output image name: ")
        hide_text(input_image_path, text, output_image_path)
        print("Text hidden successfully.")
    elif action == "find":
        input_image_path = input("Enter input image name: ")
        text_length = int(input("Enter text size: "))
        hidden_text = extract_text(input_image_path, text_length)
        print(f"Found Hidden Text: {hidden_text}")
    else:
        print("Error. Enter the correct action (hide/find)")
