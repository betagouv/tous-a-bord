from django.test import TestCase
from django.urls import resolve

from public_website import views


class TestStaticPages(TestCase):
    def test_index_url_calls_correct_view(self):
        match = resolve("/")
        self.assertEqual(match.func, views.index_view)

    def test_index_url_calls_right_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "public_website/index.html")

    def test_index_response_contains_welcome_message(self):
        response = self.client.get("/")
        self.assertContains(response, "Tous à bord !")

    def test_a11y_url_calls_correct_view(self):
        match = resolve("/accessibilite/")
        self.assertEqual(match.func, views.accessibility_view)

    def test_a11y_url_calls_right_template(self):
        response = self.client.get("/accessibilite/")
        self.assertTemplateUsed(response, "public_website/accessibility.html")

    def test_a11y_response_contains_title(self):
        response = self.client.get("/accessibilite/")
        self.assertContains(response, "Déclaration d’accessibilité")


class TestPEStatusPage(TestCase):
    def test_pestatus_url_calls_correct_view(self):
        match = resolve("/artois-mobilites/")
        self.assertEqual(match.func, views.pe_status_view)

    def test_pestatus_url_calls_right_template(self):
        response = self.client.get("/artois-mobilites/")
        self.assertTemplateUsed(response, "public_website/pe_status.html")

    def test_pestatus_response_contains_welcome_message(self):
        response = self.client.get("/artois-mobilites/")
        self.assertContains(response, "Artois Mobilités")

    def test_knownid_returns_expected_status(self):
        identifiantPE = "aflantier_1"
        response = self.client.post(
            "/artois-mobilites/", {"identifiantPE": identifiantPE}
        )
        self.assertContains(response, "identifiant : aflantier_1")

    def test_unknownid_returns_error_message(self):
        identifiantPE = "hopefullynotanexistingID"
        response = self.client.post(
            "/artois-mobilites/", {"identifiantPE": identifiantPE}
        )
        self.assertContains(response, "Situation not found")
