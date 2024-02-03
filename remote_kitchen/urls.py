
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/restaurants/', include('restaurant.urls'),),
    path('api/v1/orders/', include('orders.urls'),),
    path('api/v1/payments/', include('payments.urls'),),
    path('api-auth/', include('rest_framework.urls'))
]
