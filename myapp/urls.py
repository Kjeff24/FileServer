from django.urls import path
from django.contrib.auth import views as auth_views
from .views import homepage, user_management

urlpatterns = [
    path('', homepage.home, name='home'),
    path('signup/', user_management.signupPage, name='signup'),
    path('login/', user_management.loginPage, name='login'),
    path('logout/', user_management.logoutUser, name='logout'),
    path('activate-user/<uidb64>/<token>', user_management.activate_user, name='activate'),
    
    path(
        'reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="password/password_reset.html"), 
        name='password_reset'
    ),
    path(
        'reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_sent.html"), 
        name='password_reset_done'),
    path(
        'rese/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_form.html"), 
        name='password_reset_confirm'),
    path(
        'reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_done.html"), 
        name='password_reset_complete'),
    
    
]