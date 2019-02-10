from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('view_order', views.ViewOrder.as_view(), name='view_order'),
    path('approved', views.ApproveOrder.as_view(), name='approved')
]
