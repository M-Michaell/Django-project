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



from django.core.mail import send_mail
from django.http import JsonResponse

def send_email(request):
    admin_email = 'emailer.iti@gmail.com'
    message_to_send = {
        'subject': 'Test email from Django',
        'user_email': 'maged.khaled03@gmail.com',
        'body': 'Hello there',
    }

    # try:
    print('Try sending')
    sent_count = send_mail(
        subject=message_to_send['subject'],
        message=message_to_send['body'],
        from_email=admin_email,
        recipient_list=[message_to_send['user_email']],
        fail_silently=False,  # Set to False to catch email sending errors
    )

    if sent_count > 0:
        return JsonResponse({'status': 'Email sent successfully.'})
    else:
        return JsonResponse({'status': 'Email failed to send.'})

    # except Exception as e:
    #     return JsonResponse({'status': f'Email sending error: {str(e)}'})



# p='emailer.iti@2023'