from django.shortcuts import render
from django.urls import reverse_lazy
from account.forms import MyUserCreationForm, MyAuthenticationForm
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic.edit import CreateView


class CustomRegistrationView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account.login')  # Replace with the desired success redirect URL

    def form_valid(self, form):
        messages.success(self.request, 'Registration successful. You are now logged in.')
        user = form.save()
        # login(self.request, user)
        return super().form_valid(form)
    

class CustomLoginView(LoginView):
    authentication_form = MyAuthenticationForm
    template_name = 'account/login.html'  # Replace with the path to your login template


    def get_success_url(self):
        return reverse_lazy('account.home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('account.login') 


def userHome(request):
    return render(request, 'account/home.html')