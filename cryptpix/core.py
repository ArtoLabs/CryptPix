from PIL import Image, ImageOps
from io import BytesIO
import random


def choose_tile_size(width, height):
    max_dim = max(width, height)
    if max_dim > 1536:
        return 48
    elif max_dim > 768:
        return 24
    else:
        return 12


def distort_image(input_path):
    """
    Apply a random hue rotation (30-180 degrees) and invert colors on an image.

    Args:
        input_path: Path to the input image

    Returns:
        tuple: (PIL.Image, int) - The distorted image in memory and the chosen hue rotation
    """
    hue_rotation = random.randint(30, 180)
    img = Image.open(input_path).convert('RGB')

    hsv = img.convert('HSV')
    h, s, v = hsv.split()

    hue_shift = int((hue_rotation / 360.0) * 255)
    h_data = h.load()
    for y in range(h.size[1]):
        for x in range(h.size[0]):
            h_data[x, y] = (h_data[x, y] + hue_shift) % 256

    distorted_rgb = Image.merge('HSV', (h, s, v)).convert('RGB')
    final_image = ImageOps.invert(distorted_rgb)

    return final_image, hue_rotation


def crop_to_divisible(image, block_size):
    width, height = image.size
    new_width = width - (width % block_size)
    new_height = height - (height % block_size)
    return image.crop((0, 0, new_width, new_height))


def apply_bleed(layer, bleed=1):
    """
    Extend opaque pixels into adjacent transparent pixels to prevent
    resampling seams between checkerboard tiles.
    """
    pixels = layer.load()
    width, height = layer.size

    for _ in range(bleed):
        updates = []

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a != 0:
                    continue

                for nx, ny in (
                    (x - 1, y),
                    (x + 1, y),
                    (x, y - 1),
                    (x, y + 1),
                ):
                    if 0 <= nx < width and 0 <= ny < height:
                        rr, gg, bb, aa = pixels[nx, ny]
                        if aa != 0:
                            updates.append((x, y, (rr, gg, bb, aa)))
                            break

        for x, y, value in updates:
            pixels[x, y] = value

    return layer


def process_and_split_image(image):
    """
    Process and split an image into two layers.

    Args:
        image: PIL.Image object to process

    Returns:
        tuple: (cropped_buffer, buffer1, buffer2, block_size, width, height)
    """
    image = image.convert("RGBA")
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

    # NEW: seam-prevention bleed
    layer1 = apply_bleed(layer1, bleed=1)
    layer2 = apply_bleed(layer2, bleed=1)

    cropped_buffer = BytesIO()
    buffer1 = BytesIO()
    buffer2 = BytesIO()
    cropped_image.save(cropped_buffer, format="PNG")
    layer1.save(buffer1, format="PNG")
    layer2.save(buffer2, format="PNG")

    cropped_buffer.seek(0)
    buffer1.seek(0)
    buffer2.seek(0)

    return cropped_buffer, buffer1, buffer2, block_size, width, height
