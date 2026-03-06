from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),

    path('create/', views.lead_create, name='lead_create'),

    path('<uuid:pk>/', views.lead_detail, name='lead_detail'),

    path('<uuid:pk>/update/', views.lead_update, name='lead_update'),

    path('pipeline/', views.pipeline, name='pipeline'),
]
