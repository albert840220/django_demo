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
    path('calibrations', v.datatable_calibration),
    path('chart-js', v.chartjs, name='chart.js'),
    path('trends', v.multi_condition_plot),
    path('report_write',v.report_write),
    path('report_search',v.report_search),
    path('download/<str:form_id>', v.exportToExcel),
]

if settings.DEVEL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
