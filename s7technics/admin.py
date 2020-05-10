from django.contrib import admin

# Register your models here.
from .models import (
    AirTypes,
    Hangar,
    AviaCompany,
    AirPlane,
    TechnicalService,
    CompanyRequirement,
)


@admin.register(AirTypes)
class AirTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'length', 'width')


@admin.register(Hangar)
class HangarAdmin(admin.ModelAdmin):
    list_display = ('name', 'height', 'width', 'is_filled')


@admin.register(AviaCompany)
class AviaCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date_TS', 'end_date_TS', 'penalty_coef')


@admin.register(AirPlane)
class AirPlaneAdmin(admin.ModelAdmin):
    list_display = ('id', 'bort_number', 'plane_type', 'on_service')


@admin.register(TechnicalService)
class TechnicalServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'airplane_type', 'hangar', 'price')


@admin.register(CompanyRequirement)
class CompanyRequirementAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'service', 'require_amount', 'duration', 'contract_amount')
