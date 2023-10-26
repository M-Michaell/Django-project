from django.shortcuts import render
from django.urls import reverse_lazy
from account.forms import MyUserCreationForm, MyAuthenticationForm
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from account.models import CustomUser



def userHome(request):
    return render(request, 'account/home.html')




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


class CustomEditAccountView(UpdateView):
    model = CustomUser
    # form_class = MyUserEditForm
    fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'birthDate',
            'facebookProfile',
            'country'
        ]
    template_name = 'account/edit.html'
    success_url = reverse_lazy('account.home')  # Replace with the desired success redirect URL

    def form_valid(self, form):
        messages.success(self.request, 'Account data updated successfully.')
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        return self.request.user