from django.urls import path
from .views import CreateCheckoutSession, StripePaymentWebhook, success_view


urlpatterns = [
    path('create/', CreateCheckoutSession.as_view()),
    path('webhook/', StripePaymentWebhook.as_view()),
    path('success/', success_view, name='success'),
]
