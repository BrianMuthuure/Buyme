from django.shortcuts import get_object_or_404

from .models import Category, Product


class ProductService:
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.get(id=product_id)

    @staticmethod
    def get_all_products():
        return Product.objects.prefetch_related('productimage_set').filter(available=True)

    @staticmethod
    def get_product_by_id_and_slug(id, slug):
        product = get_object_or_404(Product, id=id, slug=slug, available=True)
        return product

