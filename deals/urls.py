from django.urls import path
from . import views

urlpatterns = [

    path(
        "pipeline/",
        views.deal_pipeline,
        name="deal_pipeline"
    ),

    path(
        "convert/<uuid:lead_id>/",
        views.convert_lead,
        name="convert_lead"
    ),

    path(
        "<uuid:deal_id>/",
        views.deal_detail,
        name="deal_detail"
    ),

    path(
        "<uuid:deal_id>/move/",
        views.move_deal_stage_view,
        name="move_deal_stage"
    ),

    path(
        "<uuid:deal_id>/won/",
        views.close_deal_won_view,
        name="close_deal_won"
    ),

    path(
        "<uuid:deal_id>/lost/",
        views.close_deal_lost_view,
        name="close_deal_lost"
    ),

    path(
        "<uuid:deal_id>/reopen/",
        views.reopen_deal_view,
        name="reopen_deal"
    )

]
