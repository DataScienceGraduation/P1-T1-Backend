from django.urls import path
from . import auth_views

urlpatterns = [
    path('signup/', auth_views.signup, name='api-signup'),
    path('signin/', auth_views.signin, name='api-login'),
    path('logout/', auth_views.logout, name='api-logout'),
    path('isAuth/', auth_views.isAuth, name='api-is-auth'),
    path('whoami/', auth_views.whoami, name='api-whoami')
]
