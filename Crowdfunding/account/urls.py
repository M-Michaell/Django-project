from django.urls import path
from account.views import CustomRegistrationView, CustomLoginView, userHome,CustomLogoutView,CustomEditAccountView

urlpatterns = [
    path('home/', userHome, name='account.home'),
    path('register/', CustomRegistrationView.as_view(), name='account.register'),
    path('login/', CustomLoginView.as_view(), name='account.login'),
    path('logout/', CustomLogoutView.as_view(), name='account.logout'),
    path('edit', CustomEditAccountView.as_view(), name='account.edit')
]
