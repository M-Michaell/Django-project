from django.shortcuts import render
from django.db.models import Sum, Count,Avg
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from project.form import Donation_form
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from project.models import Campaign, Category,Comment,Reply,Rate,Report,Donation,Tag,Image,Comment_Report
# from django.views.generic.edit import CreateView
# from project.models import Campaign
# from project.form import CreateModelForm
#
# # Create your views here.
# class CreateCampaign(CreateView):
#     model = Campaign
#     template_name = 'project/create.html'
#     form_class = CreateModelForm







def campaign_details(request,campaign_id):

    campaign = Campaign.objects.get(pk=campaign_id)
    total_donation = campaign.donation.aggregate(total_donation=Sum('donation'))['total_donation'] or 0.00
    donation_count = campaign.donation.aggregate(donation_count=Count('id'))['donation_count']
    comments = campaign.comments.all()
    campaign_images = campaign.images.all()
    tags = campaign.tags.all()
    images_all=campaign.images.all()
    rating=campaign.rate.aggregate(rate=Avg('rate'))['rate']or 0.00
    related_campaigns = Campaign.objects.filter(tags__in=tags).exclude(pk=campaign_id).distinct()[:4]
    progress =(total_donation/campaign.total_target)*100

    print(f"Campaign ID: {campaign_id}")
    print(f"Tags of Original Campaign: {list(campaign.tags.all())}")
    for c in related_campaigns:
        print(f"{c.title, c.id}")
    f_image=images_all[0]
    images=images_all[1:]

    context={
        'campaign': campaign,
        'total_donation':total_donation,
        'donation_count':donation_count,
        'comments':comments ,
        'campaign_images':campaign_images,
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
    success_url = reverse_lazy('campaign.details')