from django.urls import path
from .views import ShortURLView, ShortURLRedirectView
urlpatterns = [
    path('api/shorten/', ShortURLView.as_view(), name='shorten_url'),
    path('<str:short_url>/', ShortURLRedirectView.as_view(), name='redirect_to_original'),
]
