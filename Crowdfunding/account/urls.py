from django.urls import path
from account.views import CustomRegistrationView, CustomLoginView, userHome,CustomLogoutView,CustomEditAccountView,DeleteAccountView,activate

urlpatterns = [
    path('home/', userHome, name='account.home'),
    path('register/', CustomRegistrationView.as_view(), name='account.register'),
    path('login/', CustomLoginView.as_view(), name='account.login'),
    path('logout/', CustomLogoutView.as_view(), name='account.logout'),
    path('edit/', CustomEditAccountView.as_view(), name='account.edit'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('delete/<int:pk>/', DeleteAccountView.as_view(), name='account.delete'),


]

