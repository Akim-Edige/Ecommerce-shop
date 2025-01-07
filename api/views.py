from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from products.models import Product, Basket
from products.serializers import ProductSerializer, BasketSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import User


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()

class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductModelViewSet, self).get_permissions()

class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(Basket.objects.filter(user=self.request.user), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': 'There is no product with this ID.'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update_basket(product_id=request.data['product_id'], user=request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product_id': 'The field is required.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='delete-by-product-id')
    def remove_or_delete(self, request):
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': 'There is no product with this ID.'}, status=status.HTTP_400_BAD_REQUEST)

            is_deleted = Basket.remove_or_delete(product_id=request.data['product_id'], user=request.user)
            if is_deleted:
                return Response({'product_id': 'The product has been deleted or removed by 1.'}, status=status.HTTP_200_OK)

            return Response({'product_id': 'There is not such product in your basket.'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({'product_id': 'The field is required.'}, status=status.HTTP_400_BAD_REQUEST)


