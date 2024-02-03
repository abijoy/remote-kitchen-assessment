
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurants/', include('restaurant.urls'),),
    path('orders/', include('orders.urls'),),
    path('payments/', include('payments.urls'),),
    path('api-auth/', include('rest_framework.urls'))
]
