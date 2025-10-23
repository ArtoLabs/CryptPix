from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage


# Connect to ANY model that uses CryptPixModelMixin
@receiver(post_delete)
def delete_cryptpix_files(sender, instance, **kwargs):
    """Delete cryptpix layer files when model is deleted."""
    try:
        # Only run for models with cryptpix fields
        if hasattr(instance, 'image_layer_1'):
            if instance.image_layer_1 and default_storage.exists(instance.image_layer_1.path):
                default_storage.delete(instance.image_layer_1.path)

        if hasattr(instance, 'image_layer_2'):
            if instance.image_layer_2 and default_storage.exists(instance.image_layer_2.path):
                default_storage.delete(instance.image_layer_2.path)

    except Exception as e:
        print("CryptPix error: {}".format(e))