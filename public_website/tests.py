import factory
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve
from django.db.models import signals

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


class TestArtoisMobilitesPage(TestCase):
    @factory.django.mute_signals(signals.post_save)
    def setUp(self):
        User = get_user_model()
        self.testuser = User.objects.create_user(
            username="testuser", email="testuser@beta.fr"
        )

    def test_pestatus_url_calls_correct_view(self):
        match = resolve("/artois-mobilites/")
        self.assertEqual(match.func, views.pole_emploi_status_view)

    def test_reaching_artoismobilites_without_login_returns_redirect(self):
        response = self.client.get("/artois-mobilites/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/artois-mobilites/")

    # # BROKEN. self.client.login doesn't log in.
    # # Because of custom AUTHENTICATION_BACKENDS ?
    # def test_logged_in_user_can_reach_artoismobilites(self):
    #     login = self.client.login(
    #         username=self.testuser.username, password=self.testuser.password)
    #     self.assertTrue(login)
    #     response = self.client.get("/artois-mobilites/", follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Artois")

    # def test_pestatus_url_calls_right_template(self):
    #     response = self.client.get("/artois-mobilites/")
    #     self.assertTemplateUsed(response, "public_website/pole_emploi_status.html")

    # def test_knownid_returns_expected_status(self):
    #     identifiant_pole_emploi = "aflantier_1"
    #     response = self.client.post(
    #         "/artois-mobilites/", {"identifiant_pole_emploi": identifiant_pole_emploi}
    #     )
    #     self.assertContains(response, "identifiant : aflantier_1")

    # def test_unknownid_returns_error_message(self):
    #     identifiant_pole_emploi = "hopefullynotanexistingID"
    #     response = self.client.post(
    #         "/artois-mobilites/", {"identifiant_pole_emploi": identifiant_pole_emploi}
    #     )
    #     self.assertContains(response, "Situation not found")
