from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetView

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import LoginView,LogoutView

from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils import timezone

from django.core.mail import EmailMessage

from account.models import CustomUser
from account.tokens import account_activation_token
from account.forms import MyUserCreationForm, MyAuthenticationForm,CustomEditAccountForm, DeleteForm





class CustomRegistrationView(CreateView):
    model=CustomUser
    form_class = MyUserCreationForm
    template_name = 'account/register.html'
    # success_url = reverse_lazy('account.resend_activation') 

    def get_success_url(self):
        email = self.request.POST.get('email')
        if email:
            return reverse_lazy('account.resend_activation', kwargs={'email': email})
    

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


        self.extra_context = {'email': to_email}
        
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
        current_site = get_current_site(request)
        # return HttpResponse(f'<meta http-equiv="refresh" content="3;url={reverse_lazy("project.home")}">Thank for you registration, We will redirect you to The project after 3 seconds...')
        return render(request, 'account/redirect_active_email.html', {'redirect_url': f'{current_site.domain}/project/home'})

    
    else:
        return HttpResponse('Activation link is invalid!')
    



def resend_activation(request,email):
    if request.method == 'POST':
        email = request.POST['email']
        User = CustomUser
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'account/resend_activation.html', {'email': '','error_message': 'Email not found'})

        if user.is_active:
            return render(request, 'account/resend_activation.html', {'email': user.email,'error_message': 'User is already active'})

        current_site = get_current_site(request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('account/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return render(request, 'account/resend_activation.html', {'email': user.email,'error_message':'email send successfully'})

    return render(request, 'account/resend_activation.html', {'email': email,'error':''})






class CustomEditAccountView(UpdateView):
    model = CustomUser
    form_class = CustomEditAccountForm
    template_name = 'account/edit.html'
    success_url = reverse_lazy('project.home') 

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
        next_url = self.request.GET.get('next', None)
        if next_url:
            if next_url and next_url.startswith('/details/'):
                return next_url
            else:
                return reverse_lazy('project.home')
            



class CustomDeleteAccountView(DeleteView):
    model = CustomUser
    template_name = 'account/delete.html'  
    success_url = reverse_lazy('project.home')

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




class CustomPasswordResetView(PasswordResetView) :
    template_name='account/resetPass.html'
    pass

class CustomPasswordResetCompleteView(PasswordResetCompleteView) :
    template_name='account/completeResetPass.html'
    pass

class CustomPasswordResetConfirmView(PasswordResetConfirmView) :
    template_name='account/confirmResetPass.html'

    pass

class CustomPasswordResetDoneView(PasswordResetDoneView) :
    template_name='account/doneResetPass.html'

    pass





