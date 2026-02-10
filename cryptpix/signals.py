from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Connect to ANY model that uses CryptPixModelMixin
@receiver(post_delete)
def delete_cryptpix_files(sender, instance, **kwargs):
    """Delete CryptPix derivative files when a model instance is deleted."""
    try:
        # Layer 1 (always may exist)
        if hasattr(instance, "image_layer_1"):
            f1 = getattr(instance, "image_layer_1", None)
            name1 = getattr(f1, "name", None)
            if name1 and default_storage.exists(name1):
                default_storage.delete(name1)

        # Layer 2 (optional; may be blank when split is disabled)
        if hasattr(instance, "image_layer_2"):
            f2 = getattr(instance, "image_layer_2", None)
            name2 = getattr(f2, "name", None)
            if name2 and default_storage.exists(name2):
                default_storage.delete(name2)

    except Exception as e:
        print("CryptPix error: {}".format(e))
