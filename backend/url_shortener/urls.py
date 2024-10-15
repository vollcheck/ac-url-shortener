from django.urls import path
from .views import ShortURLView, redirect_to_original

urlpatterns = [
    path('api/shorten/', ShortURLView.as_view(), name='shorten_url'),
    path('<str:short_url>/', redirect_to_original, name='redirect_to_original'),
]
