from django.urls import path, include
from .views import CreateUserAPIView, LoginAPIView

urlpatterns = [
    path(r'create/', CreateUserAPIView.as_view()),
    path(r'login/', LoginAPIView.as_view()),
]