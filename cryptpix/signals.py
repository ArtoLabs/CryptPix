from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
import os

from cryptpix import process_and_split_image, distort_image  # Updated function that returns tile size too


class CryptPixModel:
    # Configurable attributes
    cryptpix_source_field = 'image'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Simply save the instance without additional processing
        super().save(*args, **kwargs)

@receiver(post_save, sender=CryptPixModel)
def process_cryptpix_image(sender, instance, created, **kwargs):
    """
    Signal handler to process the image after the instance is saved.
    """
    # Only process if the instance has a source image
    base_field = getattr(instance, instance.cryptpix_source_field)
    if base_field and hasattr(base_field, 'path'):
        # Perform image processing
        distorted_image, hue_rotation = distort_image(base_field.path)
        _, layer1_io, layer2_io, tile_size, width, height = process_and_split_image(distorted_image)
        base_filename = os.path.splitext(os.path.basename(base_field.name))[0]

        # Save processed layers to the respective fields
        instance.image_layer_1.save(
            f"{base_filename}_layer1.png",
            ContentFile(layer1_io.getvalue()),
            save=False
        )
        instance.image_layer_2.save(
            f"{base_filename}_layer2.png",
            ContentFile(layer2_io.getvalue()),
            save=False
        )

        # Update metadata fields
        instance.tile_size = tile_size
        instance.image_width = width
        instance.image_height = height
        instance.hue_rotation = hue_rotation

        # Save the instance with updated fields
        instance.save(update_fields=[
            'image_layer_1', 'image_layer_2', 'tile_size',
            'image_width', 'image_height', 'hue_rotation'
        ])