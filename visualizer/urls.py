from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('batches/', views.batch_view, name='batches'),
    path('batches/<batch_id>', views.batch_view, name='batches'),
]

