from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from shop.serializers import CreateUpdateProductSerializer, ProductSerializer
from shop.models import Product
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.utils import extend_schema_view
from utils.error_utils import format_errors
from utils.paginations import CustomPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


@extend_schema_view(
    list=extend_schema(
        responses={200: OpenApiResponse(response=ProductSerializer, description="Successful response")},
        description="This API endpoint retrieves a paginated list of products.",
    ),
    retrieve=extend_schema(
        responses={200: OpenApiResponse(response=ProductSerializer, description="Successful response")},
        description="This API endpoint retrieves the details of a specific product by its ID.",
    ),
    partial_update=extend_schema(
        responses={
            200: {"type": "object", "example": {"message": "ok"}},
            400: {"type": "object", "example": {"field_name": "error"}},
            500: {"type": "string", "example": "Internal server error"},
        },
        description="This API endpoint partially updates a specific product by its ID. You only need to provide the fields that you wish to update."
        "Only the fields provided in the request will be updated. Authentication and admin privileges are required to access this endpoint.",
    ),
    destroy=extend_schema(
        responses={204: None},
        description="This API endpoint destroy a specific product by its ID."
        "Only the fields provided in the request will be updated. Authentication and admin privileges are required to access this endpoint.",
    ),
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = CreateUpdateProductSerializer
    pagination_class = CustomPagination
    parser_classes = [MultiPartParser, JSONParser]

    def get_permissions(self):
        method = self.request.method
        if method == "GET":
            return [AllowAny()]
        else:
            return [IsAuthenticated(), IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSerializer
        return super().get_serializer_class()

    @extend_schema(
        request=CreateUpdateProductSerializer,
        responses={
            201: {"type": "object", "example": {"message": "ok"}},
            400: {"type": "object", "example": {"field_name": "error"}},
            500: {"type": "string", "example": "Internal server error"},
        },
        description="This API endpoint creates a new product. Provide the product details in the request body to create a new entry."
        "Only the fields provided in the request will be updated. Authentication and admin privileges are required to access this endpoint.",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        else:
            error = format_errors(serializer.errors)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            200: {"type": "object", "example": {"message": "ok"}},
            400: {"type": "object", "example": {"field_name": "error"}},
            500: {"type": "string", "example": "Internal server error"},
        },
        description="This API endpoint fully updates a specific product by its ID. Provide all product details to replace the existing data."
        "Only the fields provided in the request will be updated. Authentication and admin privileges are required to access this endpoint.",
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        else:
            error = format_errors(serializer.errors)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
