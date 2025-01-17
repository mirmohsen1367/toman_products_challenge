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


@extend_schema_view(
    list=extend_schema(responses={200: OpenApiResponse(
                                 response=ProductSerializer,
                                 description="Successful response")}),

    retrieve=extend_schema(responses={200: OpenApiResponse(
                                      response=ProductSerializer,
                                      description="Successful response")}),

    partial_update=extend_schema(responses={
        200: {"type": "object", "example": {"message": "ok"}},
        400: {"type": "object", "example": {"field_name": "error"}},
        500: {"type": "string", "example": "Internal server error"}}))

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = CreateUpdateProductSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSerializer
        return super().get_serializer_class()
    parser_classes = [MultiPartParser, JSONParser]

    @extend_schema(
    responses={
        201: {"type": "object", "example": {"message": "ok"}},
        400: {"type": "object", "example": {"field_name": "error"}},
        500: {"type": "string", "example": "Internal server error"}
    })
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
        500: {"type": "string", "example": "Internal server error"}
    })
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        else:
            error = format_errors(serializer.errors)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
