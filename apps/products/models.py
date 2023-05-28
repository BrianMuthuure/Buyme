from PIL import Image
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.products.common import user_directory_path


# Create your models here.


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    slug = models.SlugField(max_length=255, blank=True, null=True, verbose_name=_("Slug"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "categories"

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Category"))
    slug = models.SlugField(max_length=255, blank=True, null=True, verbose_name=_("Slug"))
    available = models.BooleanField(default=True, verbose_name=_("Available"))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Price"))
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Discount Price"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Is Featured"))
    is_bestseller = models.BooleanField(default=False, verbose_name=_("Is Bestseller"))
    is_new = models.BooleanField(default=False, verbose_name=_("Is New"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is Deleted"))
    brand = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Brand"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        db_table = "products"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["slug"]),
        ]

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Product"))
    image = models.ImageField(upload_to=user_directory_path, verbose_name=_("Image"))
    is_primary = models.BooleanField(default=False, verbose_name=_("Is Primary"))

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        db_table = "product_images"

    def __str__(self):
        return self.product.name

    # def save(self, *args, **kwargs):
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         new_img = (300, 300)
    #         img.thumbnail(new_img)
    #         img.save(self.image.path)
    #     super(ProductImage, self).save(*args, **kwargs)

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe("<img src='{}' height='50' />".format(self.image.url))
        else:
            return None


class Variant(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Product"))
    color = models.CharField(
        blank=True,
        null=True,
        verbose_name=_("Color"))
    size = models.CharField(
        blank=True,
        null=True,
        verbose_name=_("Size"))
    total_in_stock = models.IntegerField(
        default=0,
        verbose_name=_("Quantity"))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True, null=True,
        verbose_name=_("Price"))
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Discount Price"))

    class Meta:
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")
        db_table = "product_variants"

    def __str__(self):
        return self.product.name
