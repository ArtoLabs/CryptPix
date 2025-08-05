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

    # def save(self, *args, **kwargs):
    #     # First, save to get a primary key if needed
    #     if self.pk is None:
    #         super().save(*args, **kwargs)
    #
    #     base_field = getattr(self, self.cryptpix_source_field)
    #     if base_field and hasattr(base_field, 'path'):
    #         distorted_image, hue_rotation = distort_image(base_field.path)
    #         _, layer1_io, layer2_io, tile_size, width, height = process_and_split_image(distorted_image)
    #         base_filename = os.path.splitext(os.path.basename(base_field.name))[0]
    #
    #         self.image_layer_1.save(f"{base_filename}_layer1.png", ContentFile(layer1_io.getvalue()), save=False)
    #         self.image_layer_2.save(f"{base_filename}_layer2.png", ContentFile(layer2_io.getvalue()), save=False)
    #         self.tile_size = tile_size
    #         self.image_width = width
    #         self.image_height = height
    #         self.hue_rotation = hue_rotation
    #
    #         # Save again to persist the layers and metadata
    #         super().save(update_fields=[
    #             'image_layer_1', 'image_layer_2', 'tile_size',
    #             'image_width', 'image_height', 'hue_rotation'
    #         ])

