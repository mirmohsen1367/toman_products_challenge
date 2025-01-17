from rest_framework import serializers
from .models import Product, ProductImage
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class ProductImageSerializer(serializers.ModelSerializer):
    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise ValidationError(detail="The size image not can greater than 2M")
        return value

    class Meta:
        model = ProductImage
        fields = ("image",)


class CreateUpdateProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), allow_empty=False, write_only=True, required=False)

    def validate_images(self, images):
        if len(images) > 5:
            raise ValidationError(detail="The number of images should not be more than 5.")
        for image in images:
            if image.size > 2 * 1024 * 1024:
                raise ValidationError(detail="The size image not can greater than 2M")
        return images

    class Meta:
        model = Product
        fields = ("title", "price", "description", "images")

    def create(self, validated_data):
        product = Product.objects.create(
            title=validated_data["title"], price=validated_data["price"], description=validated_data["description"]
        )
        if "images" in validated_data:
            product_data_list = [ProductImage(image=prduct_image, product=product) for prduct_image in validated_data["images"]]
            ProductImage.objects.bulk_create(product_data_list)
        return product

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.price = validated_data.get("price", instance.price)
        instance.description = validated_data.get("description", instance.description)
        if "images" in validated_data:
            instance.product_images.all().delete()
            product_data_list = [ProductImage(image=prduct_image, product=instance) for prduct_image in validated_data["images"]]
            ProductImage.objects.bulk_create(product_data_list)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField("images_full_path")

    class Meta:
        model = Product
        fields = ("id", "title", "price", "description", "images")

    @extend_schema_field({"type": "array", "items": {"type": "string", "format": "url"}})
    def images_full_path(self, obj):
        request = self.context.get("request")
        return [request.build_absolute_uri(product_image.image.url) for product_image in obj.product_images.all()]
