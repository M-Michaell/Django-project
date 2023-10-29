from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from account.forms import MyUserCreationForm, MyAuthenticationForm,CustomEditAccountForm, DeleteForm
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from account.models import CustomUser
from django.contrib.sites.shortcuts import get_current_site
from account.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def userHome(request):
    return render(request, 'account/home.html')




class CustomRegistrationView(CreateView):
    model=CustomUser
    form_class = MyUserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account.login') 

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.activation_timestamp = timezone.now() + timezone.timedelta(hours=24)

        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('account/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        
        messages.success(self.request, 'Account data created successfully.')
        return super().form_valid(form)
    
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if user.activation_timestamp and timezone.now() > user.activation_timestamp:
            return HttpResponse('Activation link has expired.')
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
    

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


class DeleteAccountView(DeleteView):
    model = CustomUser
    template_name = 'account/delete.html'  
    success_url = reverse_lazy('account.home')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        print('inside post')
        self.object = self.get_object()
        form = DeleteForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']

            if request.user.check_password(password):
                self.object.delete()
                return redirect(self.success_url)
        
        return render(request, self.template_name, {'form': form, 'object': self.object})
    




class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('account.login') 


