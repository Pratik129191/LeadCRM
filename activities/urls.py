from django.urls import path
from . import views

urlpatterns = [

    path('today/', views.followups_today, name='followups_today'),
    path('overdue/', views.followups_overdue, name='followups_overdue'),

]