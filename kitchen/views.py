from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import DishForm
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


class CookDetailView(generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("dishes")
    template_name = "kitchen/cook-detail.html"


class DishTypeListView(generic.ListView):
    model = DishType
    paginate_by = 6
    template_name = "kitchen/dish-type-list.html"


class DishTypeCreateView(generic.CreateView):
    model = DishType
    template_name = "kitchen/dish-type-form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    fields = "__all__"


class DishTypeUpdateView(generic.UpdateView):
    model = DishType
    template_name = "kitchen/dish-type-form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    fields = "__all__"


class DishTypeDeleteView(generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish-type-confirm-delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDishListView(generic.ListView):
    model = Dish
    template_name = "kitchen/dish-type-dish-list.html"

    def get_queryset(self) -> QuerySet:
        return Dish.objects.filter(
            dish_type_id=self.kwargs["pk"]
        )


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 6
    template_name = "kitchen/dish-list.html"


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = "kitchen/dish-detail.html"
    queryset = Dish.objects.select_related("dish_type").prefetch_related("cooks")


class DishCreateView(generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish-form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish-form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish-confirm-delete.html"
    success_url = reverse_lazy("kitchen:dish-list")