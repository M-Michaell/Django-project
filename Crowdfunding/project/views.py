<<<<<<< HEAD
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, reverse


# from project.models import Campaign
# from project.form import CreateModelForm
#
# # Create your views here.
# class CreateCampaign(CreateView):
#     model = Campaign
#     template_name = 'project/create.html'
#     form_class = CreateModelForm


def profile(request):
    return render(request, template_name='project/profile.html')
=======
from django.shortcuts import render ,redirect
from django.urls import reverse_lazy ,reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.db.models import Sum, Count,Avg
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView ,DetailView
from project.form import CreateCampaignForm, CreateCategoryForm, CreateTagForm , CustomizedImageCreationForm ,Donation_form
from project.models import Campaign, Category,Comment,Reply,Rate,Report,Donation,Tag,Image,Comment_Report



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




def campaign_details(request,campaign_id):

    campaign = Campaign.objects.get(pk=campaign_id)
    total_donation = campaign.donation.aggregate(total_donation=Sum('donation'))['total_donation'] or 0.00
    donation_count = campaign.donation.aggregate(donation_count=Count('id'))['donation_count']
    comments = campaign.comments.all()
    tags = campaign.tags.all()
    images_all=campaign.image.all()
    rating=campaign.rate.aggregate(rate=Avg('rate'))['rate']or 0.00
    related_campaigns = Campaign.objects.filter(tags__in=tags).exclude(pk=campaign_id).distinct()[:4]
    progress =(total_donation/campaign.total_target)*100

    print(f"Campaign ID: {campaign_id}")
    print(f"Tags of Original Campaign: {list(campaign.tags.all())}")
    print(images_all)
    for c in related_campaigns:
        print(f"{c.title, c.id}")
    f_image=images_all[0]
    images=images_all[1:]

    context={
        'campaign': campaign,
        'total_donation':total_donation,
        'donation_count':donation_count,
        'comments':comments ,
        'tags':tags,
        'rating':rating*20,
        'f_image':f_image,
        'images':images,
        'related_campaigns':related_campaigns,
        "progress":progress
    }
    return render(request, 'project/details.html', context=context)



class CreateDonation(CreateView):
    model = Donation
    template_name = 'project/create_donation.html'
    form_class = Donation_form
    success_url = reverse_lazy('campaign.details',id='campaign_id')
    def get_success_url(self):
        return reverse('campaign.details', kwargs={'campaign_id': self.kwargs['campaign_id']})








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
    

    

>>>>>>> 58c0e9de136c4f762559f32c472f6db6d875cabc
