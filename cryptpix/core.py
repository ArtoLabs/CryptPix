from PIL import Image
from io import BytesIO

def split_image_layers(image_path, block_size=16, return_type='bytes'):
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
                    px, py = x + dx, y + dy
                    if px < width and py < height:
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
        return buffer1, buffer2
    elif return_type == 'files':
        layer1_path = f"{output_dir}/{base}_layer1.png"
        layer2_path = f"{output_dir}/{base}_layer2.png"
        layer1.save(layer1_path)
        layer2.save(layer2_path)
        return layer1_path, layer2_path



