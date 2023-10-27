from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from project.models import Campaign, Tag, Category, Image
from django.views.generic import ListView
from project.form import CreateCampaignForm, CreateCategoryForm, CreateTagForm
from django.views.generic import DetailView
from project.form import CustomizedImageCreationForm

#
# # Create your views here.
class ListAllCampaign(ListView):
    model = Campaign
    template_name = 'project/list_all_campaign.html'
    context_object_name = 'campaigns'


class CreateCampaign(CreateView):
    model = Campaign
    template_name = 'project/create_campaign.html'
    form_class = CreateCampaignForm
    success_url = reverse_lazy('project.list.all.campaign')

class CreateCategory(CreateView):
    model = Category
    template_name = 'project/create_category.html'
    form_class = CreateCategoryForm
    success_url = reverse_lazy('project.createTag')

class CreateTag(CreateView):
    model = Tag
    template_name = 'project/create_tag.html'
    form_class = CreateTagForm
    success_url = reverse_lazy('project.createCampaign')

    def form_valid(self, form):
        # Determine which button was clicked
        if 'save_button' in self.request.POST:
            self.success_url = reverse_lazy('project.createCampaign')
        elif 'other_button' in self.request.POST:
            self.success_url = reverse_lazy('project.createTag')

        return super().form_valid(form)





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
    

    


# from django.views.generic.edit import CreateView
# from project.models import Campaign
# from project.form import CreateModelForm
#
# # Create your views here.
# class CreateCampaign(CreateView):
#     model = Campaign
#     template_name = 'project/create.html'
#     form_class = CreateModelForm