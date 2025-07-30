import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from cryptpix import split_image_layers  # Updated function that returns tile size too

class CryptPixModelMixin(models.Model):
    image_layer_1 = models.ImageField(upload_to='cryptpix/', editable=False, null=True, blank=True)
    image_layer_2 = models.ImageField(upload_to='cryptpix/', editable=False, null=True, blank=True)
    tile_size = models.PositiveSmallIntegerField(editable=False, null=True, blank=True)  # NEW FIELD

    # Configurable attributes
    cryptpix_source_field = 'image'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        base_field = getattr(self, self.cryptpix_source_field)

        if is_new:
            super().save(*args, **kwargs)

        if base_field and hasattr(base_field, 'path'):
            layer1_io, layer2_io, tile_size = split_image_layers(base_field.path)  # NO MORE BLOCK SIZE PASSED IN
            base_filename = os.path.splitext(os.path.basename(base_field.name))[0]

            self.image_layer_1.save(f"{base_filename}_layer1.png", ContentFile(layer1_io.getvalue()), save=False)
            self.image_layer_2.save(f"{base_filename}_layer2.png", ContentFile(layer2_io.getvalue()), save=False)
            self.tile_size = tile_size  # STORE TILE SIZE

            update_kwargs = {k: v for k, v in kwargs.items() if k != 'force_insert'}
            super().save(*args, **update_kwargs)
        else:
            super().save(*args, **kwargs)

