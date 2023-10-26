from django.shortcuts import render
from django.urls import reverse_lazy
from account.forms import MyUserCreationForm, MyAuthenticationForm,CustomEditAccountForm
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from account.models import CustomUser




def userHome(request):
    return render(request, 'account/home.html')




class CustomRegistrationView(CreateView):
    model=CustomUser
    form_class = MyUserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account.login') 

    def form_valid(self, form):
        messages.success(self.request, 'Account data created successfully.')
        return super().form_valid(form)
    

class CustomEditAccountView(UpdateView):
    model = CustomUser
    form_class = CustomEditAccountForm
    template_name = 'account/edit.html'
    success_url = reverse_lazy('account.home') 

    def form_valid(self, form):
        if 'image' in form.cleaned_data:
            self.object.image = form.cleaned_data['image']
            self.object.save()
            
        messages.success(self.request, 'Account data updated successfully.')
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        return self.request.user
    
    
    
    

class CustomLoginView(LoginView):
    authentication_form = MyAuthenticationForm
    template_name = 'account/login.html'


    def get_success_url(self):
        return reverse_lazy('account.home')





class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('account.login') 


