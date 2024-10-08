from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("watchlists", views.watchlists, name="watchlists"),
    path("remove_item", views.remove_item, name="remove_item"),
    path("categories", views.categories, name="categories"),
    path("listed_item/<int:id>", views.listed_item, name="listed_item"),
    path("my_bid", views.my_bid, name="my_bid"),
    path("item_deleted/<int:id>", views.item_deleted, name="item_deleted"),
    path("close_bid/<int:id>", views.close_bid, name="close_bid"),
    path("comments", views.comments, name="comments"),
]
