from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("services/", views.services_view, name="services"),
    path("accessibilite/", views.accessibility_view, name="accessibilite"),
    path("artois-mobilites/", views.pole_emploi_status_view, name="artois-mobilites"),
    path(
        "brest-metropole/", views.etudiant_boursier_status_view, name="brest-metropole"
    ),
    path("mailing_webhook/<str:token>", views.mailing_view, name="mailing"),
    path("login/", views.login_view, name="login"),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("mentions-legales/", views.legal_notice_view, name="mentions-legales"),
]
