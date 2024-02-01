from django.urls import path

from .views import TodoAPIView

app_name = 'todos'

urlpatterns = [
    path('<int:pk>', TodoAPIView.as_view({'get': 'retrieve'}))
]