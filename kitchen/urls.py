from django.urls import path
from .views import index, CookListView, DishTypeListView, DishListView

urlpatterns = [
    path("", index, name="home"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("dish_types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
]

app_name = "kitchen"
