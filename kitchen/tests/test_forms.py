from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Cook, Dish, DishType

from .test_views import COOK_URL, DISHTYPE_URL, DISH_URL


class TestCookSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="usertest",
            password="password"
        )
        self.client.force_login(self.user)

    def test_search_cook(self):
        get_user_model().objects.create_user(
            username="PavloShev",
            password="password1"
        )
        get_user_model().objects.create_user(
            username="Pavlin228",
            password="password13"
        )
        get_user_model().objects.create_user(
            username="TarasShev",
            password="password12"
        )
        response = self.client.get(COOK_URL, {"username": "Pav"})
        self.assertEqual(response.status_code, 200)
        cooks = get_user_model().objects.filter(
            username__icontains="Pav"
        )
        self.assertEqual(list(response.context["cook_list"]), list(cooks))


class TestDishSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="usertest",
            password="password"
        )
        self.client.force_login(self.user)

    def test_search_dish(self):
        main_course = DishType.objects.create(name="Main Course")
        Dish.objects.create(
            name="Pepperoni Pizza",
            description="Pizza with pepperoni and mozzarella",
            price=Decimal("12.50"),
            dish_type=main_course
        )

        Dish.objects.create(
            name="Carbonara Pasta",
            description="Pasta with bacon, egg and parmesan",
            price=Decimal("14.20"),
            dish_type=main_course
        )

        Dish.objects.create(
            name="Caesar Salad",
            description="Salad with chicken, parmesan and Caesar sauce",
            price=Decimal("9.80"),
            dish_type=main_course
        )

        Dish.objects.create(
            name="Margherita Pizza",
            description="Pizza with tomato, mozzarella and basil",
            price=Decimal("10.50"),
            dish_type=main_course
        )

        response = self.client.get(DISH_URL, {"name": "Ca"})
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.filter(
            name__icontains="Ca"
        )
        self.assertEqual(list(response.context["dish_list"]), list(dishes))


class TestDishTypeSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="usertest",
            password="password"
        )
        self.client.force_login(self.user)

    def test_search_dish_type(self):
        DishType.objects.create(name="Main Course")
        DishType.objects.create(name="Salad")
        DishType.objects.create(name="Soup")
        response = self.client.get(DISHTYPE_URL, {"name": "Main"})
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.filter(
            name__icontains="Main"
        )
        self.assertEqual(list(response.context["dishtype_list"]), list(dish_types))
