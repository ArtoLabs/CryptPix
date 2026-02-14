from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

from cryptpix.html import get_css, render_image_stack, render_single_image

import json

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

            # New flags (set at save-time, treated as immutable)
            use_split = bool(getattr(photo, "use_split", False))
            use_distortion = bool(getattr(photo, "use_distortion", False))

            # Metadata (present/meaningful for split mode; hue_rotation meaningful for distortion)
            tile_size = getattr(photo, "tile_size", None)
            width = getattr(photo, "image_width", None)
            height = getattr(photo, "image_height", None)
            hue_rotation = getattr(photo, "hue_rotation", None)

            # Allow override via tag attributes
            width_attr = self.attrs.get("width")
            height_attr = self.attrs.get("height")
            breakpoints = self.attrs.get("breakpoints")
            parent_size = self.attrs.get("data-parent-size")

            if width_attr:
                width_attr = width_attr.resolve(context)
            if height_attr:
                height_attr = height_attr.resolve(context)
            if breakpoints:
                breakpoints = json.loads(breakpoints.resolve(context))
            if parent_size:
                parent_size = parent_size.resolve(context)

        except template.VariableDoesNotExist:
            return "<!-- CryptPix Error: Photo variable does not exist in context -->"
        except Exception as e:
            return f"<!-- CryptPix Error: {str(e)} -->"

        # All tag attrs (except the control/meta attrs above) get applied to the top image (split)
        # or to the single image (non-split).
        passthrough_attrs = []
        wrapper_attrs = []
        for key, val in self.attrs.items():
            if key not in ["width", "height", "breakpoints", "data-parent-size"]:
                resolved_val = val.resolve(context)
                attr_str = f'{key}="{escape(resolved_val)}"'
                passthrough_attrs.append(attr_str)
                # id and class attributes should also be applied to the wrapper div in split mode
                if key in ["id", "class"]:
                    wrapper_attrs.append(attr_str)
        passthrough_attrs_str = " ".join(passthrough_attrs)
        wrapper_attrs_str = " ".join(wrapper_attrs)

        if use_split:
            return render_image_stack(
                image_id,
                request,
                tile_size,
                width,
                height,
                hue_rotation,
                use_distortion=use_distortion,
                top_img_attrs=mark_safe(passthrough_attrs_str),
                wrapper_attrs=mark_safe(wrapper_attrs_str),
                width_attr=width_attr,
                height_attr=height_attr,
                breakpoints=breakpoints,
                parent_size=parent_size,
            )

        # Not split: render a single secure derivative (layer 1)
        return render_single_image(
            image_id,
            request,
            layer=1,
            use_distortion=use_distortion,
            hue_rotation=hue_rotation,
            img_attrs=mark_safe(passthrough_attrs_str),
            natural_width=width,
            natural_height=height,
        )
