from django.urls import include, path
from rest_framework import routers

from api.views import (BasketAdd, BasketListView, BasketRemove,
                       ProductModelViewSet, UserCreateView, UserUpdateView)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'basket', BasketRemove)
router.register(r'users', UserUpdateView)

urlpatterns = [
    path('', include(router.urls)),
    path('basket/add/', BasketAdd.as_view(), name='basket-create'),
    path('basket/', BasketListView.as_view(), name='basket-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
]
