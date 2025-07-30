import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from cryptpix import process_and_split_image  # Updated function that returns tile size too

class CryptPixModelMixin(models.Model):
    image_layer_1 = models.ImageField(upload_to='cryptpix/', editable=False, null=True, blank=True)
    image_layer_2 = models.ImageField(upload_to='cryptpix/', editable=False, null=True, blank=True)
    tile_size = models.PositiveSmallIntegerField(editable=False, null=True, blank=True)

    cryptpix_source_field = 'image'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        base_field = getattr(self, self.cryptpix_source_field)

        if is_new:
            super().save(*args, **kwargs)

        if base_field and hasattr(base_field, 'path'):
            # Process the image and get cropped image, layers, and tile size
            cropped_image_io, layer1_io, layer2_io, tile_size = process_and_split_image(base_field.path)
            base_filename = os.path.splitext(os.path.basename(base_field.name))[0]

            # Save the cropped image back to the source field
            self.cryptpix_source_field.save(f"{base_filename}.png", ContentFile(cropped_image_io.getvalue()), save=False)

            # Save the layers
            self.image_layer_1.save(f"{base_filename}_layer1.png", ContentFile(layer1_io.getvalue()), save=False)
            self.image_layer_2.save(f"{base_filename}_layer2.png", ContentFile(layer2_io.getvalue()), save=False)
            self.tile_size = tile_size

            update_kwargs = {k: v for k, v in kwargs.items() if k != 'force_insert'}
            super().save(*args, **update_kwargs)
        else:
            super().save(*args, **kwargs)

