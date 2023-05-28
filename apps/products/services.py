from django.shortcuts import get_object_or_404

from apps.products.models import Category, Product


class ProductService:
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_all_products():
        return Product.objects.prefetch_related('productimage_set').filter(available=True)

    @staticmethod
    def get_products_by_category(category_slug):
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.prefetch_related('productimage_set').filter(category=category, available=True)
        return category, products

    @staticmethod
    def get_product_by_id_and_slug(id, slug):
        product = get_object_or_404(Product, id=id, slug=slug, available=True)
        return product

