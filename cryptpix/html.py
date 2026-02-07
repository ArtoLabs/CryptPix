from django.utils.html import format_html


def render_image_stack(
    image1_url,
    image2_url,
    width,
    height,
    tile_size,
    hue_rotation,
    invert_colors=False,
):
    """
    Render two checkerboard image layers stacked correctly,
    with filtering applied at the container level and
    pixel-perfect alignment preserved.
    """

    filter_parts = []
    if invert_colors:
        filter_parts.append("invert(1)")
    if hue_rotation:
        filter_parts.append(f"hue-rotate({-hue_rotation}deg)")

    filter_style = " ".join(filter_parts)

    return format_html(
        """
        <div class="image-stack"
             style="
                --img-width:{width};
                --img-height:{height};
                aspect-ratio:{width}/{height};
                filter:{filter};
             ">
            <img src="{img1}" alt="" />
            <img src="{img2}" alt="" />

            <div class="image-meta"
                 data-tile-size="{tile}"
                 data-width="{width}"
                 data-height="{height}">
            </div>
        </div>
        """,
        img1=image1_url,
        img2=image2_url,
        width=width,
        height=height,
        tile=tile_size,
        filter=filter_style,
    )


def get_css():
    return """
    .image-stack {
        position: relative;
        display: inline-block;
        width: 100%;
        overflow: hidden;
        image-rendering: auto;
    }

    .image-stack img {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: fill;
        image-rendering: auto;
        display: block;
        pointer-events: none;
        user-select: none;
    }

    .image-meta {
        display: none;
    }
    """
