import os
import uuid
from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class Product(models.Model):
    title = models.CharField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(Decimal("2000")),
                                                                             MaxValueValidator(Decimal("9999999999"))])
    description = models.TextField()

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "product"
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ("-id",)


class ProductImage(models.Model):

    def generate_upload_path(instance, filename):
        extension = os.path.splitext(filename)[-1].lower()
        filename_base = slugify(os.path.splitext(filename)[0])
        unique_filename = f"{uuid.uuid4().hex}_{filename_base}{extension}"
        return os.path.join('product_images', str(instance.product_id), unique_filename)

    image = models.ImageField(upload_to=generate_upload_path)
    product = models.ForeignKey(to=Product, related_name="product_images", on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.product.title} - {self.id}"

    class Meta:
        db_table = "product_image"
        verbose_name = "product_image"
        verbose_name_plural = "product_images"
        ordering = ("-id",)
