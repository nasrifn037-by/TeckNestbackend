from django.urls import path
from .views import cancel_order
from . import views

urlpatterns = [
    path("products/", views.get_products),
    path("products/<int:pk>/", views.get_product),

    path("category/", views.get_Categories),

    path("cart/", views.get_Cart),
    path("cart/add/", views.add_to_Cart),
    path("cart/remove/", views.Remove_from_Cart),

    path("register/", views.register),
    path("login/", views.login),
    
    path("place-order/", views.place_order),
    path("profile/", views.profile),
    path("my-orders/",views.my_orders),
    path("profile-update/", views.profile_update),
    path("cart/update/<int:item_id>/",views.update_cart_quantity),
    path( "products/<int:product_id>/reviews/", views.product_reviews),
    path("products/<int:product_id>/add-review/",views.add_review),\
    path("cart/remove/<int:item_id>/",views.Remove_from_Cart),
    path( "cancel-order/<int:order_id>/", cancel_order),


]