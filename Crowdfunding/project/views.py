from django.shortcuts import render, redirect
from project.models import Image
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from project.form import CustomizedImageCreationForm
from django.urls import reverse_lazy, reverse


# from django.views.generic.edit import CreateView
# from project.models import Campaign
# from project.form import CreateModelForm
#
# # Create your views here.
# class CreateCampaign(CreateView):
#     model = Campaign
#     template_name = 'project/create.html'
#     form_class = CreateModelForm


def home(request):
    return render(request, 'project/home.html')

class CreateImage(CreateView):
    model = Image
    template_name = 'project/create.html'
    form_class = CustomizedImageCreationForm
    success_url = reverse_lazy("project.home")

    def form_valid(self, form):
        # Determine which button was clicked
        if 'save' in self.request.POST:
            self.success_url = reverse_lazy('project.home')
        elif 'add' in self.request.POST:
            self.success_url = reverse_lazy('images.create')

        return super().form_valid(form)


class DeleteImage(DeleteView):
    model = Image
    template_name = 'accounts/delete.html'
    success_url = reverse_lazy('project.home')

class EditProfileView(UpdateView):
   model = Image
   template_name = 'project/edit.html'
   form_class = CustomizedImageCreationForm
   success_url = reverse_lazy('project.home')

class ImageView(DetailView):
    model = Image
    template_name = 'project/view.html'
    context_object_name = 'image'
    def get_object(self, queryset=None):
        return self.request.user
    

    