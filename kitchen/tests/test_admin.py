from django.test import TestCase
from django.urls import reverse

from kitchen.models import Cook


class TestAdmin(TestCase):
    def setUp(self):
        self.admin_user = Cook.objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.cook = Cook.objects.create_user(
            username="cook",
            password="None123",
            first_name="Test",
            last_name="TestLast",
            years_of_experience=2
        )

    def test_years_of_experience_in_list_display(self):
        url = reverse("admin:kitchen_cook_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_years_of_experience_by_pk(self):
        url = reverse("admin:kitchen_cook_change", args=[self.cook.pk])
        response = self.client.get(url)
        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_add(self):
        url = reverse("admin:kitchen_cook_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "years_of_experience")
