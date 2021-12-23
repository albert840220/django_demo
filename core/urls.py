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
    path('addnew',v.addnew),
    path('edit/<int:id>', v.edit),
    path('update/<int:id>', v.update),
    path('delete/<int:id>', v.destroy),
    path('transactions1', v.trans),
    path('datatable-test', v.show_datatable),
]

if settings.DEVEL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
