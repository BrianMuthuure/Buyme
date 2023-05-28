from django.contrib import admin
from django.utils.html import format_html

from .common import S3Handler
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
            safe_url = S3Handler.create_presigned_url(primary_image.image.name)
            return format_html(f'<a href="{safe_url}" target="_blank">{primary_image.image.name}</a>')
        return None

    primary_image_url.short_description = 'Primary Image URL'

    def product_variant(self, obj):
        variants = obj.variant_set.all()
        if variants:
            variant_ids = [variant.id for variant in variants]
            return variant_ids
        return None

    product_variant.short_description = 'Product Variant'
