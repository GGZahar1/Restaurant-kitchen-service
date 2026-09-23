from django.contrib.auth.models import AbstractUser
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.PositiveIntegerField()

    REQUIRED_FIELDS = ["years_of_experience"]

    def __str__(self) -> str:
        return (f"{self.username} (first_name={self.first_name}, last_name={self.last_name},"
                f" years_of_experience={self.years_of_experience})")


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.PROTECT)
    cooks = models.ManyToManyField(Cook, related_name="dishes")

    def __str__(self) -> str:
        return f"{self.name} (price={self.price}, dish_type={self.dish_type.name})"
