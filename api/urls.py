from django.urls import path
from . import auth_views
from . import product_views
from . import order_views

urlpatterns = [
    path('signup/', auth_views.signup, name='api-signup'),
    path('signin/', auth_views.signin, name='api-login'),
    path('logout/', auth_views.logout, name='api-logout'),
    path('isAuth/', auth_views.isAuth, name='api-is-auth'),
    path('whoami/', auth_views.whoami, name='api-whoami'),
    path('getCart/', order_views.getCart, name='api-get-cart'),
    path('deleteCart/', order_views.deleteCart, name='api-delete-cart'),
    path('addToCart/', order_views.addToCart, name='api-add-to-cart'),
    path('getOrders/', order_views.getOrders, name='api-get-orders'),
    path('getOrder/', order_views.getOrder, name='api-get-order'),
    path('addImageToProduct/', order_views.addImageToProduct, name='api-add-image-to-product'),
    path('getFeaturedProducts/', product_views.getFeaturedProducts, name='api-get-featured-products'),
    path('getProducts/', product_views.getProducts, name='api-get-products'),
    path('getProduct/', product_views.getProduct, name='api-get-product'),
    path('getCategories/', product_views.getCategories, name='api-get-categories'),
    path('search/', product_views.Search, name='api-search')
]
