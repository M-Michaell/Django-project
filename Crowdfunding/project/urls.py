from django.urls import path
from project.views import campaign_details,CreateDonation
from project.views import home
from project.views import ListAllCampaign, CreateCampaign,  CreateCategory, ListAllCategory

urlpatterns = [
    path('list_all/', ListAllCampaign.as_view(), name="project.list.all.campaign"),
    # path('craete_tag/', CreateTag.as_view(), name="project.createTag"),
    path('craete_category/', CreateCategory.as_view(), name="project.createCategory"),
    path('craete_campaign/',CreateCampaign.as_view(), name="project.createCampaign"),
    path('details/<int:campaign_id>', campaign_details,name="campaign.details"),
    path('donation/<int:campaign_id>', CreateDonation.as_view(),name="campaign.donation"),
    path('home/', ListAllCategory.as_view(), name = 'project.home'),
    # path('uploadImage/', CreateImage.as_view(), name='images.create'),
    # path('viewImage/', ImageView.as_view(), name='images.show'),
    ]
