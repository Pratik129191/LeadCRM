from django.urls import path
from . import views

urlpatterns = [

    path(
        "pipeline/",
        views.deal_pipeline,
        name="deal_pipeline"
    ),

]

