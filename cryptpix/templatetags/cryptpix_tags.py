from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
import json

from cryptpix.html import get_css, render_image_stack

register = template.Library()


@register.simple_tag
def cryptpix_css():
    return mark_safe(get_css())


@register.tag
def cryptpix_image(parser, token):
    bits = token.split_contents()
    tag_name = bits[0]

    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            f"'{tag_name}' tag requires at least 1 argument: photo instance"
        )

    photo_var = parser.compile_filter(bits[1])
    raw_attrs = bits[2:]

    attrs = {}
    for bit in raw_attrs:
        if "=" not in bit:
            raise template.TemplateSyntaxError(f"Malformed attribute assignment: {bit}")
        key, val = bit.split("=", 1)
        attrs[key] = parser.compile_filter(val)

    return CryptPixImageNode(photo_var, attrs)


class CryptPixImageNode(template.Node):
    def __init__(self, photo_var, attrs):
        self.photo_var = photo_var
        self.attrs = attrs

    def render(self, context):
        request = context.get("request")

        try:
            photo = self.photo_var.resolve(context)

            image_id = getattr(photo, "pk", None)
            tile_size = getattr(photo, "tile_size", None)
            width = getattr(photo, "image_width", None)
            height = getattr(photo, "image_height", None)
            hue_rotation = getattr(photo, "hue_rotation", None)

            # Tag overrides / options
            width_attr = self.attrs.get("width")
            height_attr = self.attrs.get("height")
            breakpoints = self.attrs.get("breakpoints")

            # Back-compat: consumers use data-parent-size="true"
            parent_size = (
                self.attrs.get("data-parent-size")
                or self.attrs.get("parent-size")
                or self.attrs.get("parent_size")
            )

            if width_attr:
                width_attr = width_attr.resolve(context)
            if height_attr:
                height_attr = height_attr.resolve(context)

            if breakpoints:
                raw = breakpoints.resolve(context)
                # Allow either a JSON string or a real Python list/dict
                if isinstance(raw, (list, dict)):
                    breakpoints = raw
                else:
                    breakpoints = json.loads(raw)

            if parent_size:
                parent_size = parent_size.resolve(context)

        except template.VariableDoesNotExist:
            return "<!-- CryptPix Error: Photo variable does not exist in context -->"
        except Exception as e:
            return f"<!-- CryptPix Error: {escape(str(e))} -->"

        # Attributes passed to the old "top <img>" now apply to the container.
        # IMPORTANT: do NOT forward sizing-control attributes here, or they will conflict.
        excluded = {
            "width",
            "height",
            "breakpoints",
            "data-parent-size",
            "parent-size",
            "parent_size",
        }

        container_attrs = []
        for key, val in self.attrs.items():
            if key in excluded:
                continue
            resolved_val = val.resolve(context)
            container_attrs.append(f'{key}="{escape(resolved_val)}"')

        container_attrs_str = " ".join(container_attrs)

        return render_image_stack(
            image_id,
            request,
            tile_size,
            width,
            height,
            hue_rotation,
            top_img_attrs=mark_safe(container_attrs_str),
            width_attr=width_attr,
            height_attr=height_attr,
            breakpoints=breakpoints,
            parent_size=parent_size,
        )
