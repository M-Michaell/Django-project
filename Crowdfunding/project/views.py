from django.shortcuts import render
# from django.views.generic.edit import CreateView
# from project.models import Campaign
# from project.form import CreateModelForm
#
# # Create your views here.
# class CreateCampaign(CreateView):
#     model = Campaign
#     template_name = 'project/create.html'
#     form_class = CreateModelForm

def test(request):
    return render(request, 'project/create.html')