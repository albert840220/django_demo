# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include  # add this
from electrodes import views as v

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path('electrodes/', include("electrodes.urls")),  # Django electrodes route
    path("", include("app.urls")),  # UI Kits Html files
    path("", include("authentication.urls")),  # Auth routes - login / register
    path('calibrations', v.tables_calibration),
    path('chart-js', v.chartjs, name='chart.js'),
    path('trends', v.multi_condition_plot),
    path('report_write', v.report_write),
    path('tables_report', v.tables_report),
    path('download/<str:form_id>', v.exportToExcel),
    path('call_it', v.call_it),
    path('welcome', v.welcome, name="home page"),
    path('equipment/ph', v.tables_ph_parts),
    path('equipment/ph/new', v.add_equipment_ph),
    # path('dayuse',v.days_used), #零件時數表，顯示"已使用天數"
    path("equipment/ph/<str:sn>", v.equipment_ph_detail),
    path("customer", v.tables_customer),
    path("customer/new", v.add_customer),
    path("equipment", v.equipment_type),
    path("pre_repair", v.tables_pre_repair),
    path("schedule/<str:sn>", v.add_job),
    # path("schedule/cod/<str:sn>", v.add_job),
    path("schedule", v.tables_pm_schedule),
    # path("pm_schedule/add_job", v.default_work_schedule),
    path("schedule/close/<str:id>", v.close_case),
    path("survey/new", v.form_customer_survey),
    path("png/<str:id>", v.display_png),
    path("survey", v.tables_customer_survey),
    path("business", v.tables_business_schedule),
    path("business/new", v.form_business_schedule),

]

if settings.DEVEL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
