Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from PIL import Image
... 
... # Function to encode text into an image
... def encode_text(image_path, secret_text, output_path):
...     # Open an image file
...     img = Image.open(image_path)
...     width, height = img.size
... 
...     # Ensure the text can fit into the image
...     max_bytes_to_hide = (width * height * 3) // 8
...     if len(secret_text) > max_bytes_to_hide:
...         raise ValueError("Text too large to hide in image")
... 
...     # Encode each character as a 7-bit binary ASCII value
...     # Use the least significant bits of each pixel RGB components
...     binary_secret_text = ''.join(format(ord(char), '07b') for char in secret_text)
...     if len(binary_secret_text) > max_bytes_to_hide * 8:
...         raise ValueError("Text too large to hide in image")
... 
...     data_index = 0
...     # Encode pixels in the image
...     for x in range(width):
...         for y in range(height):
...             r, g, b = img.getpixel((x, y))
... 
...             # Modify the least significant bit only if there is still data to store
...             if data_index < len(binary_secret_text):
...                 # Least significant red pixel bit
...                 img.putpixel((x, y), (r & 254 | int(binary_secret_text[data_index]), g, b))
...                 data_index += 1
...             if data_index < len(binary_secret_text):
...                 # Least significant green pixel bit
...                 img.putpixel((x, y), (r, g & 254 | int(binary_secret_text[data_index]), b))
...                 data_index += 1
            if data_index < len(binary_secret_text):
                # Least significant blue pixel bit
                img.putpixel((x, y), (r, g, b & 254 | int(binary_secret_text[data_index])))
                data_index += 1

            # If data has been encoded, save the image and return
            if data_index >= len(binary_secret_text):
                img.save(output_path)
                return

    # If reached here, not enough space to encode
    raise ValueError("Image size too small to hide data")

# Function to decode text from an image
def decode_text(image_path):
    # Open an image file
    img = Image.open(image_path)
    width, height = img.size

    binary_secret_text = ""

    # Extract encoded text from the image pixels
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))

            # Extracting least significant bit from each pixel component
            binary_secret_text += bin(r)[-1]
            binary_secret_text += bin(g)[-1]
            binary_secret_text += bin(b)[-1]

    # Convert binary text to ASCII characters
    secret_text = ""
    for i in range(0, len(binary_secret_text), 7):
        byte = binary_secret_text[i:i + 7]
        secret_text += chr(int(byte, 2))

    return secret_text

# Example usage:
if __name__ == "__main__":
    # Encode text into an image
    image_path = "example_photo.jpg"
    output_image_path = "output_encoded_image.png"
    secret_text = "This is a secret message hidden in the photo."

    try:
        encode_text(image_path, secret_text, output_image_path)
        print("Text encoded successfully.")

        # Decode text from the encoded image
        decoded_text = decode_text(output_image_path)
        print("Decoded text:", decoded_text)

    except ValueError as e:
        print(e)
