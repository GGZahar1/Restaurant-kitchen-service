from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import generic

from kitchen.models import Dish, DishType, Cook


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_dish": Dish.objects.count(),
        "num_dish_type": DishType.objects.count(),
        "num_cooks": get_user_model().objects.count()
    }
    return render(request, "kitchen/index.html", context=context)


class CookListView(generic.ListView):
    model = Cook
    paginate_by = 6
    template_name = "kitchen/cook-list.html"


class DishTypeListView(generic.ListView):
    model = DishType
    paginate_by = 6
    template_name = "kitchen/dish-type-list.html"


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 6
    template_name = "kitchen/dish-list.html"

