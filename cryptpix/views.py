import os
from django.conf import settings
from django.http import FileResponse, HttpResponseForbidden, HttpResponseNotFound
import django.apps

from .utils import unsign_image_token, get_cryptpix_models



def secure_image_view(request, signed_value):

    image_id, signed_session_key = unsign_image_token(signed_value, max_age=5)

    if image_id is None or signed_session_key != request.session.session_key:
        return HttpResponseForbidden("Invalid or expired link.")

    # Parse the image ID - assuming format: "model_pk_layer" (e.g. "product_123_1")
    try:
        pk_layer = image_id.split('_')
        if len(pk_layer) != 2:
            raise ValueError("Invalid image_id format")
        pk, layer = pk_layer
        layer = int(layer)
        pk = int(pk)

        # Find the matching model
        for model in get_cryptpix_models():
            try:
                instance = model.objects.get(pk=pk)
                if layer == 0:
                    # Access the original image field using the cryptpix_source_field attribute
                    field_name = instance.cryptpix_source_field
                    image_field = getattr(instance, field_name)
                    if image_field:
                        return FileResponse(image_field.open('rb'), content_type='image/jpeg')
                elif layer == 1 and instance.image_layer_1:
                    return FileResponse(instance.image_layer_1.open('rb'), content_type='image/jpeg')
                elif layer == 2 and instance.image_layer_2:
                    return FileResponse(instance.image_layer_2.open('rb'), content_type='image/jpeg')
            except model.DoesNotExist:
                pass
    except (ValueError, AttributeError):
        pass

    return HttpResponseNotFound("Image not found.")
