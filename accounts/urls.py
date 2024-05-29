from django.urls import path
from . import views

urlpatterns = [
    path('auth/register', views.RegisterView.as_view(), name='user-register'),
    path('auth/login', views.LoginView.as_view(), name='user-login'),
    path('user/profile/<int:pk>',
         views.UserProfileView.as_view(), name='user-profile'),
    path('user/delete-account', views.delete_account, name='user-delete')
]
