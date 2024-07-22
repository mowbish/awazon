from django.urls import path, include
from apps.products.api.v1.views import ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
