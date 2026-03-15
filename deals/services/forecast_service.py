from django.db.models import Sum, F, FloatField, ExpressionWrapper
from ..models import Deal


class ForecastService:
    @staticmethod
    def pipeline_expected_revenue(organization):
        weighted_value = ExpressionWrapper(
            F("value") * F("stage__probability") / 100.0,
            output_field=FloatField(),
        )

        result = Deal.objects.filter(
            organization=organization,
            stage__is_closed=False
        ).annotate(
            expected_value=weighted_value
        ).aggregate(
            total_expected=Sum("expected_value")
        )

        return result["total_expected"] or 0


    @staticmethod
    def stage_forecast(organization):
        weighted_value = ExpressionWrapper(
            F("value") * F("stage__probability") / 100.0,
            output_field=FloatField(),
        )

        deals = Deal.objects.filter(
            organization=organization,
            stage__is_closed=False
        ).annotate(
            expected_value=weighted_value
        )

        stage_summary = {}

        for deal in deals:
            stage_name = deal.stage.name
            if stage_name not in stage_summary:
                stage_summary[stage_name] = 0
            stage_summary[stage_name] += float(deal.expected_value)

        return stage_summary









