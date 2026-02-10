import os

from django.core.files.base import ContentFile
from django.db import models

from cryptpix import process_and_split_image, distort_image


class CryptPixModelMixin(models.Model):
    cp_dir = "cryptpix/%Y-%m-%d-%H-%M"

    # Security toggles (set at save-time; if you want different settings, delete + re-upload)
    use_split = models.BooleanField(default=True)
    use_distortion = models.BooleanField(default=True)

    # Stored derivatives
    image_layer_1 = models.ImageField(
        upload_to=cp_dir, editable=False, null=True, blank=True, max_length=500
    )
    image_layer_2 = models.ImageField(
        upload_to=cp_dir, editable=False, null=True, blank=True, max_length=500
    )

    # Split metadata (only meaningful when use_split=True)
    tile_size = models.PositiveSmallIntegerField(editable=False, null=True, blank=True)
    image_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    image_height = models.PositiveIntegerField(editable=False, null=True, blank=True)

    # Distortion metadata (only meaningful when use_distortion=True)
    hue_rotation = models.PositiveSmallIntegerField(editable=False, null=True, blank=True)

    # Configurable attributes
    cryptpix_source_field = "image"

    class Meta:
        abstract = True

    def _save_derivative_to_field(self, field, base_filename: str, suffix: str, content: bytes) -> str:
        filename = f"{base_filename}_{suffix}.png"
        path = field.field.generate_filename(self, filename)
        field.storage.save(path, ContentFile(content))
        field.name = path
        return path

    def save(self, *args, **kwargs):
        # Save first to ensure PK exists (upload_to may depend on instance state)
        if self.pk is None:
            super().save(*args, **kwargs)

        base_field = getattr(self, self.cryptpix_source_field, None)

        # Only generate derivatives once (no regeneration/toggle changes supported)
        if base_field and hasattr(base_field, "path") and not self.image_layer_1:
            base_filename = os.path.splitext(os.path.basename(base_field.name))[0]

            hue_rotation = None

            # Start from the source image on disk
            if self.use_distortion:
                working_image, hue_rotation = distort_image(base_field.path)
            else:
                # If we are not distorting, we still need a PIL image object for split/non-split saves.
                # Reuse distort_image's loader pattern by calling PIL directly here.
                from PIL import Image  # local import to keep import surface small

                working_image = Image.open(base_field.path).convert("RGBA")

            if self.use_split:
                # Split mode: always produces two layers
                _, layer1_io, layer2_io, tile_size, width, height = process_and_split_image(working_image)

                self._save_derivative_to_field(
                    self.image_layer_1, base_filename, "layer1", layer1_io.getvalue()
                )
                self._save_derivative_to_field(
                    self.image_layer_2, base_filename, "layer2", layer2_io.getvalue()
                )

                self.tile_size = tile_size
                self.image_width = width
                self.image_height = height

            else:
                # Non-split mode: store a single processed image in layer_1, keep layer_2 empty
                from io import BytesIO  # local import
                buf = BytesIO()
                working_image.save(buf, format="PNG")
                buf.seek(0)

                self._save_derivative_to_field(
                    self.image_layer_1, base_filename, "layer1", buf.getvalue()
                )

                # Explicitly keep layer 2 empty and clear split metadata
                if self.image_layer_2:
                    self.image_layer_2.delete(save=False)
                self.image_layer_2 = None
                self.tile_size = None
                self.image_width = None
                self.image_height = None

            # Set/clear distortion metadata
            self.hue_rotation = hue_rotation if self.use_distortion else None

            update_fields = [
                "use_split",
                "use_distortion",
                "image_layer_1",
                "image_layer_2",
                "tile_size",
                "image_width",
                "image_height",
                "hue_rotation",
            ]

            # Keep existing behavior: if the concrete model has a thumbnail field, let it be updated too
            if hasattr(self, "thumbnail") and self.thumbnail:
                update_fields.append("thumbnail")

            super().save(update_fields=update_fields)
            return

        super().save(*args, **kwargs)
