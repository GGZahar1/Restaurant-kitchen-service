from django.urls import path
from django.views import View

from .views import index, CookListView, DishTypeListView, DishListView, DishDetailView, CookDetailView, \
    DishTypeDishListView, DishCreateView, DishUpdateView, DishDeleteView

urlpatterns = [
    path("", index, name="home"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("dish_types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("dish-types/<int:pk>/dishes/", DishTypeDishListView.as_view(), name="dish-type-dishes-list"),

]

app_name = "kitchen"
