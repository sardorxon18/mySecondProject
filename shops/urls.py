from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page, name="homepage"),
    path("detail/<int:pk>/", views.detail_page, name="product_detail"),
    # dsanfdsjnvjsdbnvds;vnadsvja
    path("filter/expensive/", views.filter_expensive, name="filter_expensive"),
    path("filter/cheap/", views.filter_cheap, name="filter_cheap"),
    path("filter/likes/", views.filter_likes, name="filter_likes"),
    path("all-product", views.all_product, name="all_product"),
    path("new-arrivals", views.new_arrivals, name="new_arrivals"),
    path("popular-item", views.popular_item, name="popular_item"),
    

]
