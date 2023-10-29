from django.urls import path,include
from account.views import CustomRegistrationView, CustomLoginView,CustomLogoutView,CustomEditAccountView,CustomDeleteAccountView,activate
from account.views import CustomPasswordResetCompleteView,CustomPasswordResetConfirmView,CustomPasswordResetDoneView,CustomPasswordResetView,resend_activation
from account.views import csrf_failure_redirect,PasswordResetErrorView

urlpatterns = [
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
    path('resend_activation/<email>/', resend_activation, name='account.resend_activation'),
    path('csrf_failure/', csrf_failure_redirect, name='csrf_failure_redirect'),

    # path('social-auth/', include('social_django.urls', namespace='social')),
    path('password_reset_error/', PasswordResetErrorView.as_view(), name='password_reset_error'),




]

