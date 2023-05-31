from django.urls import path
from .views import homepage, user_management

urlpatterns = [
    path('', homepage.home, name='home'),
    path('signup/', user_management.signupPage, name='signup'),
    path('login/', user_management.loginPage, name='login'),
    path('activate-user/<uidb64>/<token>', user_management.activate_user, name='activate'),
]