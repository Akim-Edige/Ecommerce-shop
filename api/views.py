from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from products.models import Basket, Product
from products.serializers import (BasketAddUpdateSeriaizer,
                                  BasketViewSerializer, ProductSerializer)
from users.models import User
from users.serializers import UserSerializer
from users.tasks import send_email_verification


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_email_verification(user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserUpdateView(GenericViewSet, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
            if user.id != request.user.id:
                return Response({'User': "You can not update someone else's info"}, status=status.HTTP_404_NOT_FOUND)

            return super(UserUpdateView, self).update(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response({'User': "There is no such user"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
            if user.id != request.user.id:
                return Response({'User': "You can not delete someone else's account"}, status=status.HTTP_404_NOT_FOUND)

            return super(UserUpdateView, self).destroy(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response({'User': "There is no such user"}, status=status.HTTP_404_NOT_FOUND)


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductModelViewSet, self).get_permissions()


class BasketListView(ListAPIView):
    serializer_class = BasketViewSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(Basket.objects.filter(user=self.request.user), many=True)
        return Response(serializer.data)


class BasketAdd(CreateAPIView):
    serializer_class = BasketAddUpdateSeriaizer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product': 'There is no product with this ID.'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update_basket(product_id=request.data['product'], user=request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = BasketViewSerializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product': 'The field is required. Put product ID'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'product': 'The field is required. Put product ID'}, status=status.HTTP_400_BAD_REQUEST)


class BasketRemove(GenericViewSet):
    queryset = Basket.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BasketAddUpdateSeriaizer

    @action(detail=False, methods=['post'], url_path='remove')
    def basket_remove(self, request):
        try:
            product_id = request.data['product']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product': 'There is no product with this ID.'}, status=status.HTTP_400_BAD_REQUEST)

            is_deleted = Basket.remove_or_delete(product_id=request.data['product'], user=request.user)
            if is_deleted:
                return Response({'product': 'The product has been deleted or removed by 1.'}, status=status.HTTP_200_OK)

            return Response({'product': 'There is not such product in your basket.'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({'product': 'The field is required. Put product ID'}, status=status.HTTP_400_BAD_REQUEST)
