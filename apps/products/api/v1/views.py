from django.core.cache import cache
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.products.models import Product
from apps.products.api.v1.serializers import ProductSerializer
from apps.products.utils import scrape_product_data


class ProductViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        asin = kwargs.get(self.lookup_field)

        product_data = cache.get(asin)
        if product_data:
            return Response(product_data)

        product = self.get_queryset().filter(asin=asin).first()
        if product:
            serializer = self.get_serializer(product)
            cache.set(asin, serializer.data, timeout=86400)  # Cache for 1 day
            return Response(serializer.data)

        product_data = scrape_product_data(asin)
        if product_data:
            serializer = self.get_serializer(data=product_data)
            if serializer.is_valid():
                serializer.save()
                cache.set(asin, serializer.data, timeout=86400)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)