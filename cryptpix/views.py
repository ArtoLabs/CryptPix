import mimetypes

from django.http import FileResponse, HttpResponseForbidden, HttpResponseNotFound

from .utils import unsign_image_token, get_cryptpix_models


def _guess_content_type(file_field) -> str:
    """
    Best-effort content type guess based on filename.
    Falls back to 'application/octet-stream' if unknown.
    """
    name = getattr(file_field, "name", "") or ""
    content_type, _ = mimetypes.guess_type(name)
    return content_type or "application/octet-stream"


def secure_image_view(request, signed_value):
    image_id, signed_session_key = unsign_image_token(signed_value, max_age=1200)

    if image_id is None or signed_session_key != request.session.session_key:
        return HttpResponseForbidden("Invalid or expired link.")

    # image_id format: "{pk}_{layer}" (e.g. "123_1")
    try:
        pk_layer = image_id.split("_")
        if len(pk_layer) != 2:
            raise ValueError("Invalid image_id format")

        pk_str, layer_str = pk_layer
        pk = int(pk_str)
        layer = int(layer_str)

        for model in get_cryptpix_models():
            try:
                instance = model.objects.get(pk=pk)

                # Layer 0: original source image field
                if layer == 0:
                    field_name = instance.cryptpix_source_field
                    image_field = getattr(instance, field_name, None)
                    if image_field:
                        return FileResponse(
                            image_field.open("rb"),
                            content_type=_guess_content_type(image_field),
                        )

                # Layer 1: always served from image_layer_1 (exists for all processed variants)
                if layer == 1 and instance.image_layer_1:
                    return FileResponse(
                        instance.image_layer_1.open("rb"),
                        content_type=_guess_content_type(instance.image_layer_1),
                    )

                # Layer 2: only valid/servable when split is enabled
                if layer == 2:
                    if getattr(instance, "use_split", False) and instance.image_layer_2:
                        return FileResponse(
                            instance.image_layer_2.open("rb"),
                            content_type=_guess_content_type(instance.image_layer_2),
                        )
                    return HttpResponseNotFound("Image not found.")

            except model.DoesNotExist:
                continue

    except (ValueError, AttributeError, TypeError):
        pass

    return HttpResponseNotFound("Image not found.")
