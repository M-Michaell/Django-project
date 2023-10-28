from django.urls import path
from account.views import CustomRegistrationView, CustomLoginView, userHome,CustomLogoutView,CustomEditAccountView,CustomDeleteAccountView,activate
from account.views import CustomPasswordResetCompleteView,CustomPasswordResetConfirmView,CustomPasswordResetDoneView,CustomPasswordResetView

urlpatterns = [
    path('home/', userHome, name='account.home'),
    path('register/', CustomRegistrationView.as_view(), name='account.register'),
    path('login/', CustomLoginView.as_view(), name='account.login'),
    path('logout/', CustomLogoutView.as_view(), name='account.logout'),
    path('edit/', CustomEditAccountView.as_view(), name='account.edit'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('delete/<int:pk>/', CustomDeleteAccountView.as_view(), name='account.delete'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


]

