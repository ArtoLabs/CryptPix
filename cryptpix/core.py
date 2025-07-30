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

# Here in case we expand to include this option in the future
def crop_to_divisible(image, block_size):
    width, height = image.size
    new_width = width - (width % block_size)
    new_height = height - (height % block_size)
    return image.crop((0, 0, new_width, new_height))


def resize_to_divisible(image, block_size):
    width, height = image.size
    new_width = width - (width % block_size)  # or round up: (width // block_size + 1) * block_size
    new_height = height - (height % block_size)  # or round up: (height // block_size + 1) * block_size
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # LANCZOS for high-quality resizing


def split_image_layers(image_path, return_type='bytes', output_dir='.', base='output'):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    block_size = choose_tile_size(width, height)
    image = resize_to_divisible(image, block_size)
    width, height = image.size

    layer1 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    layer2 = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    original_pixels = image.load()
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

    if return_type == 'bytes':
        buffer1 = BytesIO()
        buffer2 = BytesIO()
        layer1.save(buffer1, format="PNG")
        layer2.save(buffer2, format="PNG")
        buffer1.seek(0)
        buffer2.seek(0)
        return buffer1, buffer2, block_size
    elif return_type == 'files':
        layer1_path = os.path.join(output_dir, f"{base}_layer1.png")
        layer2_path = os.path.join(output_dir, f"{base}_layer2.png")
        layer1.save(layer1_path)
        layer2.save(layer2_path)
        return layer1_path, layer2_path, block_size




