import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from cryptpix import process_and_split_image, distort_image  # Updated function that returns tile size too

class CryptPixModelMixin(models.Model):
    image_layer_1 = models.ImageField(upload_to='cryptpix/', editable=False, null=True, blank=True)
    image_layer_2 = models.ImageField(upload_to='cryptpix/', editable=False, null=True, blank=True)
    tile_size = models.PositiveSmallIntegerField(editable=False, null=True, blank=True)
    image_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    image_height = models.PositiveIntegerField(editable=False, null=True, blank=True)
    hue_rotation = models.PositiveSmallIntegerField(editable=False, null=True, blank=True)

    # Configurable attributes
    cryptpix_source_field = 'image'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        base_field = getattr(self, self.cryptpix_source_field)

        if base_field and hasattr(base_field, 'path'):
            # Distort the image and get the random hue rotation
            distorted_image, hue_rotation = distort_image(base_field.path)
            # Process the image and get cropped image, layers, and tile size
            _, layer1_io, layer2_io, tile_size, width, height = process_and_split_image(distorted_image)
            base_filename = os.path.splitext(os.path.basename(base_field.name))[0]

            # Save the layers
            self.image_layer_1.save(f"{base_filename}_layer1.png", ContentFile(layer1_io.getvalue()), save=False)
            self.image_layer_2.save(f"{base_filename}_layer2.png", ContentFile(layer2_io.getvalue()), save=False)
            self.tile_size = tile_size
            self.image_width = width
            self.image_height = height
            self.hue_rotation = hue_rotation

            update_kwargs = {k: v for k, v in kwargs.items() if k != 'force_insert'}
            super().save(*args, **update_kwargs)

        super().save(*args, **kwargs)

