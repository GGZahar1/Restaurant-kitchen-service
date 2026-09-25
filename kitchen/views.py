from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import DishForm, CookForm, DishSearchForm, DishTypeSearchForm, CookSearchForm
from kitchen.models import Dish, DishType, Cook


@login_required
def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_dish": Dish.objects.count(),
        "num_dish_type": DishType.objects.count(),
        "num_cooks": get_user_model().objects.count()
    }
    return render(request, "kitchen/index.html", context=context)


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 6
    template_name = "kitchen/cook-list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            queryset = Cook.objects.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("dishes")
    template_name = "kitchen/cook-detail.html"


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookForm
    template_name = "kitchen/cook-form.html"


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = ("username", "first_name", "last_name", "years_of_experience")
    template_name = "kitchen/cook-form.html"


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "kitchen/cook-confirm-delete.html"
    success_url = reverse_lazy("kitchen:cook-list")


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    paginate_by = 6
    template_name = "kitchen/dish-type-list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            queryset = DishType.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    template_name = "kitchen/dish-type-form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    fields = "__all__"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "kitchen/dish-type-form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    fields = "__all__"


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish-type-confirm-delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "kitchen/dish-type-dish-list.html"

    def get_queryset(self) -> QuerySet:
        return Dish.objects.filter(
            dish_type_id=self.kwargs["pk"]
        )


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 6
    template_name = "kitchen/dish-list.html"
    queryset = Dish.objects.select_related("dish_type")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            queryset = Dish.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish-detail.html"
    queryset = Dish.objects.select_related("dish_type").prefetch_related("cooks")


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish-form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish-form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish-confirm-delete.html"
    success_url = reverse_lazy("kitchen:dish-list")


@login_required
def toggle_assign_to_dish(request, pk):
    cook = request.user
    dish = Dish.objects.get(id=pk)

    if dish in cook.dishes.all():
        cook.dishes.remove(dish)
    else:
        cook.dishes.add(dish)

    return redirect("kitchen:dish-detail", pk=pk)
