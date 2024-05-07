from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='api-signup'),
    path('signin/', views.signin, name='api-login'),
    path('logout/', views.logout, name='api-logout'),
    path('isAuth/', views.isAuth, name='api-is-auth'),
    path('whoami/', views.whoami, name='api-whoami'),
]
