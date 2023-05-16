from django.contrib import admin
from .models import Product, Category, ProductImage, Variant


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['id', 'image_tag']
    extra = 2
    classes = ['collapse']
    show_change_link = True


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 2
    classes = ['collapse']
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
    list_display = ['name', 'slug', 'category', 'price', 'available', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
