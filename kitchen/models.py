from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return (f"{self.username} (first_name={self.first_name},"
                f" last_name={self.last_name},"
                f" years_of_experience={self.years_of_experience})")

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.PROTECT)
    cooks = models.ManyToManyField(Cook, related_name="dishes", blank=True)

    def __str__(self) -> str:
        return (f"{self.name} (price={self.price},"
                f" dish_type={self.dish_type.name})")
