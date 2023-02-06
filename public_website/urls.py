from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("accessibilite/", views.accessibility_view, name="accessibilite"),
    path("artois-mobilites/", views.pe_status_view, name="artoismobi")
]
