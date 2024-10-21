from PIL import Image


def extract_message(image_path, length):
    img = Image.open(image_path)
    width, height = img.size
    binary_message = ""
    index = 0
    for y in range(height):
        if index > length:
            break
        for x in range(width):
            if index > length:
                break
            pixel = list(img.getpixel((x, y)))
            for i in range(3):
                if index < length:
                    binary_message += str(pixel[i] & 1)
                    index += 1
                else:
                    break
    print(binary_message)
    extracted_chars = []
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        char_code = int(byte, 2)
        extracted_chars.append(chr(char_code))
    return ''.join(extracted_chars)


image_path = 'ComfyUI_01034_.png'
extracted_message = extract_message(image_path, 168)
print(extracted_message)
