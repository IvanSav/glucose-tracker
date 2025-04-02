from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LevelViewSet, upload_glucose_csv

router = DefaultRouter()
router.register(r"levels", LevelViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("upload-glucose/", upload_glucose_csv, name="upload_glucose_csv"),
]
