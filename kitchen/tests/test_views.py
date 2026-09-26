from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish, DishType

DISH_URL = reverse("kitchen:dish-list")
DISHTYPE_URL = reverse("kitchen:dish-type-list")
COOK_URL = reverse("kitchen:cook-list")


class PublicDishTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DISH_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testusername",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_list(self):
        test_dish_type = DishType.objects.create(name="Test")
        Dish.objects.create(
            name="TEST",
            price=Decimal("10.00"),
            description="TEST",
            dish_type=test_dish_type
        )
        Dish.objects.create(
            name="Test2",
            price=Decimal("10.12"),
            description="ABC",
            dish_type=test_dish_type
        )
        response = self.client.get(DISH_URL)
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(list(response.context["dish_list"]), list(dishes))
        self.assertTemplateUsed(response, "kitchen/dish-list.html")


class PublicDishTypeTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DISHTYPE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testusername",
            password="None2234"
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_type_list(self):
        DishType.objects.create(name="Test1")
        DishType.objects.create(name="Test2")
        response = self.client.get(DISHTYPE_URL)
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(response.context["dishtype_list"]),
            list(dish_types)
        )
        self.assertTemplateUsed(response, "kitchen/dish-type-list.html")


class PublicCookTest(TestCase):
    def test_login_required(self):
        response = self.client.get(COOK_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCookTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_cook_list(self):
        get_user_model().objects.create_user(
            username="testusername",
            password="TestPassword"
        )
        get_user_model().objects.create_user(
            username="testusername12",
            password="TestPassword1"
        )
        response = self.client.get(COOK_URL)
        self.assertEqual(response.status_code, 200)
        cooks = get_user_model().objects.all()
        self.assertEqual(list(response.context["cook_list"]), list(cooks))
        self.assertTemplateUsed(response, "kitchen/cook-list.html")
