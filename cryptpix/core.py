from PIL import Image
from io import BytesIO

from PIL import Image
from io import BytesIO
import os


def choose_tile_size(width, height):
    max_dim = max(width, height)
    if max_dim > 1536:
        return 48
    elif max_dim > 768:
        return 24
    else:
        return 12


def crop_to_divisible(image, block_size):
    width, height = image.size
    new_width = width - (width % block_size)
    new_height = height - (height % block_size)
    return image.crop((0, 0, new_width, new_height))


def process_and_split_image(image_path):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    block_size = choose_tile_size(width, height)
    cropped_image = crop_to_divisible(image, block_size)
    width, height = cropped_image.size

    layer1 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    layer2 = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    original_pixels = cropped_image.load()
    pixels1 = layer1.load()
    pixels2 = layer2.load()

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            use_first_layer = ((x // block_size) + (y // block_size)) % 2 == 0
            for dy in range(block_size):
                for dx in range(block_size):
                    px, py = x + dx, y + dy
                    pixel = original_pixels[px, py]
                    if use_first_layer:
                        pixels1[px, py] = pixel
                    else:
                        pixels2[px, py] = pixel

    # Save cropped image and layers to BytesIO
    cropped_buffer = BytesIO()
    buffer1 = BytesIO()
    buffer2 = BytesIO()
    cropped_image.save(cropped_buffer, format="PNG")
    layer1.save(buffer1, format="PNG")
    layer2.save(buffer2, format="PNG")
    cropped_buffer.seek(0)
    buffer1.seek(0)
    buffer2.seek(0)

    return cropped_buffer, buffer1, buffer2, block_size




