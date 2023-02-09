from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("accessibilite/", views.accessibility_view, name="accessibilite"),
    path("artois-mobilites/", views.pe_status_view, name="artois-mobilites"),
    path("login/", views.login_view, name="login"),
    path("oidc/", include("mozilla_django_oidc.urls")),
]
