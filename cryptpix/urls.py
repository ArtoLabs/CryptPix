from django.urls import path
from .views import secure_image_view

urlpatterns = [
    path('secure-image/<str:signed_value>/', secure_image_view, name='secure-image'),
]
