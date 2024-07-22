from django.urls import include, path

urlpatterns = [
    path("products/", include("apps.products.api.v1.urls")),
    path("users/", include("apps.users.api.v1.urls")),
]
