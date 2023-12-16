from PIL import Image

def map_pixels_to_ascii(image, ascii_chars):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ascii_chars[pixel//25 - 1]
    return ascii_str

def main(image_path, new_width=100):
    ascii_chars = "@%#*+=-:. "  # Define ASCII characters from dark to light

    try:
        image = Image.open(image_path)
    except Exception as e:
        print(e)
        return

    # Convert image to grayscale
    image = image.convert("L")

    # Resize image
    width, height = image.size
    height = height/2
    aspect_ratio = height/float(width)
    new_height = int(aspect_ratio * new_width)
    image = image.resize((new_width, new_height))

    # Convert image pixels to ascii
    ascii_str = map_pixels_to_ascii(image, ascii_chars)
    
    # Format the ASCII art
    img_ascii = [ascii_str[index:index+new_width] for index in range(0, len(ascii_str), new_width)]
    return "\n".join(img_ascii)

# Run the program
ascii_art = main("brainScan.jpg")  # Replace with your image path
print()
print()
print()
print()
print()
print()

print(ascii_art)

print()
print()
print()
print()
print()
print()
print()
