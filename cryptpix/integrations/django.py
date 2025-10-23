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
        # First, save to get a primary key if needed
        if self.pk is None:
            super().save(*args, **kwargs)

        base_field = getattr(self, self.cryptpix_source_field)
        if base_field and hasattr(base_field, 'path') and not self.image_layer_1:
            distorted_image, hue_rotation = distort_image(base_field.path)
            _, layer1_io, layer2_io, tile_size, width, height = process_and_split_image(distorted_image)
            base_filename = os.path.splitext(os.path.basename(base_field.name))[0]

            # Generate filenames with upload_to applied
            layer1_filename = f"{base_filename}_layer1.png"
            layer1_path = self.image_layer_1.field.generate_filename(self, layer1_filename)
            layer2_filename = f"{base_filename}_layer2.png"
            layer2_path = self.image_layer_2.field.generate_filename(self, layer2_filename)

            # Save files directly to storage
            self.image_layer_1.storage.save(layer1_path, ContentFile(layer1_io.getvalue()))
            self.image_layer_2.storage.save(layer2_path, ContentFile(layer2_io.getvalue()))

            # Set field names
            self.image_layer_1.name = layer1_path
            self.image_layer_2.name = layer2_path

            self.tile_size = tile_size
            self.image_width = width
            self.image_height = height
            self.hue_rotation = hue_rotation

            cryptpix_fields = [
                'image_layer_1', 'image_layer_2', 'tile_size',
                'image_width', 'image_height', 'hue_rotation'
            ]

            if self.thumbnail:
                cryptpix_fields.append('thumbnail')

            super().save(update_fields=cryptpix_fields)
        else:
            super().save(*args, **kwargs)

