"""Core image-processing utilities for CryptPix.

This module is intentionally framework-agnostic (no Django imports).

Concepts
  - Distortion: random hue rotation (30–180 degrees) + RGB inversion.
  - Split: checkerboard tiling split into two RGBA layers.

The Django model mixin can use these helpers to generate either:
  - a single processed image (optionally distorted), or
  - two split layers (optionally distorted before splitting).
"""

from __future__ import annotations

import random
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple, Union

from PIL import Image, ImageOps


PILImageOrPath = Union[Image.Image, str, Path]


def choose_tile_size(width: int, height: int) -> int:
    """Pick a tile size based on max dimension."""
    max_dim = max(width, height)
    if max_dim > 1536:
        return 48
    if max_dim > 768:
        return 24
    return 12


def _open_image(image_or_path: PILImageOrPath) -> Image.Image:
    if isinstance(image_or_path, Image.Image):
        return image_or_path
    return Image.open(str(image_or_path))


def distort_image(image_or_path: PILImageOrPath) -> Tuple[Image.Image, int]:
    """Apply a random hue rotation (30–180 degrees) and invert colors.

    Accepts either a PIL Image or a filesystem path.

    Returns:
        (distorted_image_rgb, hue_rotation_degrees)
    """
    hue_rotation = random.randint(30, 180)
    img = _open_image(image_or_path).convert("RGB")

    # Convert to HSV
    hsv = img.convert("HSV")
    h, s, v = hsv.split()

    # Apply hue rotation (Pillow hue is 0–255, so scale accordingly)
    hue_shift = int((hue_rotation / 360.0) * 255)
    h_data = h.load()
    for y in range(h.size[1]):
        for x in range(h.size[0]):
            h_data[x, y] = (h_data[x, y] + hue_shift) % 256

    # Reconstruct and convert back to RGB
    distorted_rgb = Image.merge("HSV", (h, s, v)).convert("RGB")

    # Invert colors
    final_image = ImageOps.invert(distorted_rgb)
    return final_image, hue_rotation


def crop_to_divisible(image: Image.Image, block_size: int) -> Image.Image:
    """Crop image so width/height are divisible by block_size."""
    width, height = image.size
    new_width = width - (width % block_size)
    new_height = height - (height % block_size)
    return image.crop((0, 0, new_width, new_height))


def _image_to_png_bytes(image: Image.Image) -> BytesIO:
    buf = BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return buf


def process_and_split_image(image: Image.Image):
    """Split an image into two checkerboard layers.

    Args:
        image: PIL.Image to split

    Returns:
        (cropped_buffer, layer1_buffer, layer2_buffer, block_size, width, height)
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

    cropped_buffer = _image_to_png_bytes(cropped_image)
    buffer1 = _image_to_png_bytes(layer1)
    buffer2 = _image_to_png_bytes(layer2)
    return cropped_buffer, buffer1, buffer2, block_size, width, height


def build_cryptpix_layers(
    source: PILImageOrPath,
    *,
    use_distortion: bool,
    use_split: bool,
) -> Tuple[BytesIO, Optional[BytesIO], Optional[int], int, int, Optional[int]]:
    """Generate the derivative(s) CryptPix stores.

    Convenience wrapper around distortion + splitting.

    Contract:
      - If use_split is True: returns (layer1, layer2, tile_size, w, h, hue_rotation)
      - If use_split is False: returns (layer1, None, None, w, h, hue_rotation)

    Notes:
      - Returned images are PNG BytesIO objects.
      - hue_rotation is only returned when use_distortion is True.
    """
    img = _open_image(source)
    hue_rotation: Optional[int] = None

    if use_distortion:
        img, hue_rotation = distort_image(img)

    if use_split:
        _, layer1_io, layer2_io, tile_size, width, height = process_and_split_image(img)
        return layer1_io, layer2_io, tile_size, width, height, hue_rotation

    # Not split: store a single PNG derivative in layer 1
    img_rgba = img.convert("RGBA")
    width, height = img_rgba.size
    layer1_io = _image_to_png_bytes(img_rgba)
    return layer1_io, None, None, width, height, hue_rotation
