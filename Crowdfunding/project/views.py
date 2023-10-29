from django.shortcuts import render ,redirect
from django.urls import reverse_lazy ,reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db.models import Sum, Count,Avg
from django.views.generic import ListView ,DetailView
from project.form import CreateCampaignForm, CreateCategoryForm ,Donation_form
from project.models import Campaign, Category,Comment,Reply,Rate,Report,Donation,Comment_Report
from django.contrib.auth.models import  User
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class ListAllCampaign(ListView):
    model = Campaign
    template_name = 'project/list_all_campaign.html'
    context_object_name = 'campaigns'


class CreateCampaign(LoginRequiredMixin,CreateView):
    model = Campaign
    template_name = 'project/create_campaign.html'
    form_class = CreateCampaignForm
    success_url = reverse_lazy('project.list.all.campaign')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class DeleteCampaign(DeleteView):
    model = Campaign
    template_name = 'project/delete.html'
    context_object_name = "campaign"
    success_url = reverse_lazy('project.list.all.campaign')

class EditCampaign(UpdateView):
    model = Campaign
    template_name = 'project/edit_campaign.html'
    context_object_name = "campaign"
    form_class = CreateCampaignForm
    success_url = reverse_lazy('project.list.all.campaign')

class CreateCategory(CreateView):
    model = Category
    template_name = 'project/create_category.html'
    form_class = CreateCategoryForm
    success_url = reverse_lazy('project.home')


class ListAllCategory(ListView):
    model = Category
    template_name = 'project/home.html'
    context_object_name = 'cats'



def campaign_details(request,campaign_id):

    campaign = Campaign.objects.get(pk=campaign_id)
    total_donation = campaign.donation.aggregate(total_donation=Sum('donation'))['total_donation'] or 0.00
    donation_count = campaign.donation.aggregate(donation_count=Count('id'))['donation_count']
    comments = campaign.comments.all()
    tags = campaign.tags.all()
    # images_all=campaign.image.all()
    rating=campaign.rate.aggregate(rate=Avg('rate'))['rate']or 0.00
    related_campaigns = Campaign.objects.filter(tags__in=tags).exclude(pk=campaign_id).distinct()[:4]
    progress =(float(total_donation)/float(campaign.total_target))*100.00

    print(f"Campaign ID: {campaign_id}")
    print(f"Tags of Original Campaign: {list(campaign.tags.all())}")
    # print(images_all)
    for c in related_campaigns:
        print(f"{c.title, c.id}")
    # f_image=images_all[0]
    # images=images_all[1:]

    context={
        'campaign': campaign,
        'total_donation':total_donation,
        'donation_count':donation_count,
        'comments':comments ,
        'tags':tags,
        'rating':rating*20,
        # 'f_image':f_image,
        # 'images':images,
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



def profile(request):
    return render(request, template_name='project/profile.html')


