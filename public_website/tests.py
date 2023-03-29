import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import signals
from django.test import TestCase
from django.urls import resolve

from public_website import views
from public_website.utils import obfuscate


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


class TestServicesPage(TestCase):
    @factory.django.mute_signals(signals.post_save)
    def setUp(self):
        User = get_user_model()
        self.testuser = User.objects.create_user(
            username="testuser", email="testuser@beta.fr"
        )
        artois_mobilites_group = Group.objects.create(name="Artois Mobilités")
        artois_mobilites_group.user_set.add(self.testuser)

    def test_pestatus_url_calls_correct_view(self):
        match = resolve("/artois-mobilites/")
        self.assertEqual(match.func, views.pole_emploi_status_view)

    def test_reaching_artoismobilites_without_login_returns_redirect(self):
        response = self.client.get("/artois-mobilites/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/")

    def test_reaching_artoismobilites_without_login_returns_error_message(self):
        response = self.client.get("/artois-mobilites/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/login/")
        expected_message = "Vous devez être connecté·e pour accéder à cette page"
        self.assertContains(response, expected_message)

    def test_logged_in_user_can_reach_services(self):
        self.client.force_login(self.testuser)
        response = self.client.get("/services/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Services")

    def test_authorized_group_can_reach_view(self):
        self.client.force_login(self.testuser)
        response = self.client.get("/artois-mobilites/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Interface d'interrogation de l'API Pôle Emploi")

    def test_wrong_group_cant_reach_view(self):
        self.client.force_login(self.testuser)
        response = self.client.get("/brest-metropole/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/services/")
        error_message = "Le groupe associé n&#x27;a pas l&#x27;autorisation d&#x27;accéder à la page."
        self.assertContains(response, error_message)

    def test_pestatus_url_calls_expected_template(self):
        self.client.force_login(self.testuser)
        response = self.client.get("/artois-mobilites/")
        self.assertTemplateUsed(response, "public_website/pole_emploi_status.html")

    def test_knownid_returns_expected_status(self):
        self.client.force_login(self.testuser)
        identifiant_pole_emploi = "aflantier_1"
        response = self.client.post(
            "/artois-mobilites/",
            {"identifiant_pole_emploi": identifiant_pole_emploi},
            follow=True,
        )
        self.assertContains(response, "Flantier")

    def test_unknownid_returns_error_message(self):
        self.client.force_login(self.testuser)
        identifiant_pole_emploi = "hopefullynotanexistingID"
        response = self.client.post(
            "/artois-mobilites/", {"identifiant_pole_emploi": identifiant_pole_emploi}
        )

        self.assertContains(response, "Situation not found")


class TestUtils(TestCase):
    def test_obfuscate_email(self):
        result_positive = obfuscate.obfuscate_email("benoit.serrano@beta.gouv.fr")
        self.assertEqual(result_positive, "**************@beta.gouv.fr")

        result_negative = obfuscate.obfuscate_email("benoit.serranobeta.gouv.fr")
        self.assertEqual(result_negative, "**************************")
