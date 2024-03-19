from django.urls import include, path

from config import settings
from public_website import api, views

print(settings)
urlpatterns = [
    path("", views.index_view, name="index"),
    path("services/", views.services_view, name="services"),
    path("accessibilite/", views.accessibility_view, name="accessibilite"),
    path("artois-mobilites/", views.pole_emploi_status_view, name="artois-mobilites"),
    path("demo/", views.demo_view, name="demo"),
    path("demo/export/select", views.demo_export_select_view, name="demo/import"),
    path("demo/import", views.demo_import_index_view),
    path("demo/imports/", views.demo_imports_index_view, name="demo/imports"),
    path("demo/import/<int:id>/", views.demo_import_item_view),
    path(
        "brest-metropole/", views.etudiant_boursier_status_view, name="brest-metropole"
    ),
    path("login/", views.login_view, name="login"),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("mentions-legales/", views.legal_notice_view, name="mentions-legales"),
    path(f"api/webhook/{settings.GRIST_WEBHOOK_SECRET}", api.webhook, name="webhook"),
]
