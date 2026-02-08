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
    Render CryptPix image layers using a single paint context via
    CSS background layers to guarantee pixel-perfect alignment.
    """

    filter_parts = []
    if invert_colors:
        filter_parts.append("invert(1)")
    if hue_rotation:
        filter_parts.append(f"hue-rotate({-hue_rotation}deg)")

    filter_style = " ".join(filter_parts)

    background_style = (
        f"background-image: url('{image1_url}'), url('{image2_url}');"
        "background-size: 100% 100%, 100% 100%;"
        "background-position: 0 0, 0 0;"
        "background-repeat: no-repeat, no-repeat;"
    )

    return format_html(
        """
        <div class="image-stack"
             style="
                --img-width:{width};
                --img-height:{height};
                aspect-ratio:{width}/{height};
                {background}
                filter:{filter};
             ">
            <div class="image-meta"
                 data-tile-size="{tile}"
                 data-width="{width}"
                 data-height="{height}">
            </div>
        </div>
        """,
        width=width,
        height=height,
        tile=tile_size,
        filter=filter_style,
        background=background_style,
    )


def get_css():
    return """
    .image-stack {
        position: relative;
        display: inline-block;
        width: 100%;
        overflow: hidden;
        background-color: transparent;
        image-rendering: auto;
        pointer-events: none;
        user-select: none;
    }

    .image-meta {
        display: none;
    }
    """
