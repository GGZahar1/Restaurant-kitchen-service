from django.urls import path
from .views import index, CookListView, DishTypeListView, DishListView, DishDetailView, CookDetailView

urlpatterns = [
    path("", index, name="home"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("dish_types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail")
]

app_name = "kitchen"
