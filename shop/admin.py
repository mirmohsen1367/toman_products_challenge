from django.contrib import admin
from .models import Product, ProductImage
from django.forms import BaseInlineFormSet, ValidationError


class ProductImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            if not form.cleaned_data.get("image") and not form.cleaned_data.get("DELETE", False):
                raise ValidationError("Image cannot be blank. Please upload an image or delete the form.")
        if len(self.cleaned_data) > 5:
            raise ValidationError("The number of images should not be more than 5.")
        for image in self.cleaned_data:
            if image["image"].size > 2 * 1024 * 1024:
                raise ValidationError("The size image not can greater than 2M")


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    formset = ProductImageInlineFormSet


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price"]
    search_fields = ("title",)
    inlines = [ProductImageAdmin]


admin.site.register(Product, ProductAdmin)
