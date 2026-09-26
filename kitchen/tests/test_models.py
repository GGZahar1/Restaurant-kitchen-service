from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import Dish, DishType


class ModelsTest(TestCase):
    def test_dish_str(self):
        test_dish_type = DishType.objects.create(name="Test Dish Type")
        dish = Dish.objects.create(
            name="Dish",
            description="Test Description",
            price=Decimal("12.22"),
            dish_type=test_dish_type
        )
        self.assertEqual(
            str(dish),
            f"{dish.name} (price={dish.price},"
            f" dish_type={dish.dish_type.name})"
        )

    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="Test")
        self.assertEqual(str(dish_type), dish_type.name)

    def test_cook_str(self):
        username = "Test"
        password = "Testpassword"
        years_of_experience = 12
        first_name = "Testfirstname"
        last_name = "Testlastname"
        test_cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience,
            first_name=first_name,
            last_name=last_name
        )
        self.assertEqual(
            str(test_cook),
            f"{username} (first_name={first_name}, last_name={last_name},"
            f" years_of_experience={years_of_experience})"
        )

    def test_cook_years_of_experience(self):
        username = "Test"
        password = "password"
        years_of_experience = 12
        cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )
        self.assertEqual(cook.username, username)
        self.assertTrue(cook.check_password(password))
        self.assertEqual(cook.years_of_experience, years_of_experience)
