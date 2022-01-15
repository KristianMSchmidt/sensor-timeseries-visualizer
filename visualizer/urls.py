from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('timeseries/<batch_id>', views.timeseries_view, name='timeseries'),
    path('load_data/', views.load_data_view, name="load_data")
]

