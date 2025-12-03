from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.ab_test_view, name='ab_test_view'),
    path('click/', views.ab_test_click, name='ab_test_click'),
]
