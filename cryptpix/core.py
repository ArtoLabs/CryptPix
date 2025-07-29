from PIL import Image
import os

def split(image_path, block_size=10):
    """Splits an image into two interlocking transparent layers."""
    image = Image.open(image_path).convert("RGBA")
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
                    px = x + dx
                    py = y + dy
                    if px < width and py < height:
                        pixel = original_pixels[px, py]
                        if use_first_layer:
                            pixels1[px, py] = pixel
                        else:
                            pixels2[px, py] = pixel

    return layer1, layer2
