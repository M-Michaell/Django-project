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