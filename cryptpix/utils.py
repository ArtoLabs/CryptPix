from django.core.signing import TimestampSigner
from .integrations.django import CryptPixModelMixin


signer = TimestampSigner()

def sign_image_token(image_id, user_id):
    value = f"{image_id}:{user_id}"
    return signer.sign(value)

def unsign_image_token(signed_value, max_age=300):
    # 5 minutes default expiry
    from django.core.signing import SignatureExpired, BadSignature
    try:
        value = signer.unsign(signed_value, max_age=max_age)
        image_id, user_id = value.split(":")
        return image_id, int(user_id)
    except (SignatureExpired, BadSignature):
        return None, None


def get_cryptpix_models():
    models = []
    for model in django.apps.apps.get_models():
        if issubclass(model, CryptPixModelMixin) and model is not CryptPixModelMixin:
            models.append(model)
    return models
