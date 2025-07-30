import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from cryptpix import split_image_layers  # the function you renamed from split()

class CryptPixModelMixin(models.Model):
    # These are the only fields we define
    image_layer_1 = models.ImageField(upload_to='cryptpix/', editable=False, null=True, blank=True)
    image_layer_2 = models.ImageField(upload_to='cryptpix/', editable=False, null=True, blank=True)

    # Configurable attributes
    cryptpix_source_field = 'image'         # Name of the base image field
    cryptpix_block_size = 48                # Default block size

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        base_field = getattr(self, self.cryptpix_source_field)

        if is_new:
            super().save(*args, **kwargs)

        if base_field and hasattr(base_field, 'path'):
            layer1_io, layer2_io = split_image_layers(
                base_field.path,
                block_size=self.cryptpix_block_size
            )
            base_filename = os.path.splitext(os.path.basename(base_field.name))[0]

            self.image_layer_1.save(f"{base_filename}_layer1.png", ContentFile(layer1_io.getvalue()), save=False)
            self.image_layer_2.save(f"{base_filename}_layer2.png", ContentFile(layer2_io.getvalue()), save=False)

            update_kwargs = {k: v for k, v in kwargs.items() if k != 'force_insert'}
            super().save(*args, **update_kwargs)
        else:
            super().save(*args, **kwargs)
