
from django.urls import path, include
from .views import RestaurantList, RestaurantDetail, MenuList, MenuDetail, ItemList, ItemDetail

urlpatterns = [
    path('', RestaurantList.as_view(), name='restaurants'),
    path('<int:pk>/', RestaurantDetail.as_view(), name='restaurant-detail'),
    path('<int:pk>/menus/', MenuList.as_view(), name='menus'),
    path('<int:pk>/menus/<int:menu_id>/', MenuDetail.as_view(), name='menu-detail'),
    path('<int:pk>/menus/<int:menu_id>/items/', ItemList.as_view(), name='items'),
    path('<int:pk>/menus/<int:menu_id>/items/<int:item_id>/', ItemDetail.as_view(), name='item-detail'),

    # path('api-auth/', include('rest_framework.urls'))
]
