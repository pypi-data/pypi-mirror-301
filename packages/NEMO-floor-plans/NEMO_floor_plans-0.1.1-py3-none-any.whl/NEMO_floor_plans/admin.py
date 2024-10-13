from django.contrib import admin
from NEMO.mixins import ModelAdminRedirectMixin

from NEMO_floor_plans.models import FloorPlan, FloorPlanIcon, FloorPlanNode


@admin.register(FloorPlan)
class FloorPlanAdmin(ModelAdminRedirectMixin, admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(FloorPlanNode)
class FloorPlanNodeAdmin(ModelAdminRedirectMixin, admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(FloorPlanIcon)
class FloorPlanIconAdmin(ModelAdminRedirectMixin, admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request)
