from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Product, Category, ProductImage, Variant


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['id', 'image_tag']
    extra = 2
    show_change_link = True


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 2
    show_change_link = True
    readonly_fields = ['id']

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [VariantInline, ProductImageInline]
    list_display = [
        'name', 'category', 'price', 'primary_image_url',
        'available', 'created_at', 'updated_at', 'product_variant']
    prepopulated_fields = {'slug': ('name',)}

    def primary_image_url(self, obj):
        primary_image = obj.productimage_set.filter(is_primary=True).first()
        if primary_image:
            return format_html('<a href="{}" target="_blank">Primary image url</a>', primary_image.image.url)
        return None

    primary_image_url.short_description = 'Primary Image URL'

    def product_variant(self, obj):
        variants = obj.variant_set.all()
        if variants:
            variant_ids = [variant.id for variant in variants]
            return variant_ids
        return None

    product_variant.short_description = 'Product Variant'
