from django.urls import path
from project.views import campaign_details,CreateDonation

urlpatterns = [
    # path('create/', CreateCampaign.as_view(), name="project.create"),
    path('details/<int:campaign_id>', campaign_details,name="campaign.details"),
    path('donation/<int:campaign_id>', CreateDonation.as_view(),name="campaign.donation"),
]
