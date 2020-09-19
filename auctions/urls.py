from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing/", views.create_listing_view, name="create_listing"),
    path("show_listing/<int:listing_id>/", views.show_listing_view, name="show_listing"),
    path("show_watchlist/", views.show_watchlist_view, name="show_watchlist"),
    path("show_watchlist/remove/<int:watchlist_item_id>/", views.remove_from_watchlist_view, name="remove_from_watchlist"),
    path("show_watchlist/add/<int:listing_item_id>/", views.add_to_watchlist_view, name="add_to_watchlist"),
    path("show_watchlist/<int:listing_id>/add_bid/", views.add_bid_to_listing_view, name="add_bid_to_listing"),
    path("show_watchlist/<int:listing_id>/add_comment/", views.add_comment_to_listing_view, name="add_comment_to_listing"),
    path("show_watchlist/<int:listing_id>/close_auction/", views.close_auction_view, name="close_auction"),
    path("show_categories/", views.show_categories_view, name="show_categories"),
    path("show_category/<int:category_id>/", views.show_category_items_view, name="show_category_items"),
]
