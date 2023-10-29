from django.urls import path
from project.views import campaign_details,CreateDonation
from project.views import DeleteCampaign, ListAllCampaign, EditCampaign ,CreateCampaign,  CreateCategory, ListAllCategory
from project.views import home, profile
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('list_all/', ListAllCampaign.as_view(), name="project.list.all.campaign"),
    path('craete_category/', CreateCategory.as_view(), name="project.createCategory"),
    path('craete_campaign/',CreateCampaign.as_view(), name="project.createCampaign"),
    path('details/<int:campaign_id>', campaign_details,name="campaign.details"),
    path('donation/<int:campaign_id>', CreateDonation.as_view(),name="campaign.donation"),
    path('home/', ListAllCategory.as_view(), name = 'project.home'),
    path('home/', home, name = 'project.home'),
    path('profile/', profile, name="project.profile"),
    path('<int:pk>/delete', login_required(DeleteCampaign.as_view()), name="project.deleteCampaign"),
    path('<int:pk>/edit', login_required(EditCampaign.as_view()), name="project.editCampaign")

]

