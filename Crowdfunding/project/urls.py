from django.urls import path
# from project.views import CreateCampaign
from project.views import campaign_details,CreateDonation
from project.views import home 
from project.views import  CreateCampaign, CreateCategory 
from project.views import home, profile
from project.views import CreateCampaign,  CreateCategory, home, featured, latest, search, CategoryDetailView



urlpatterns = [
    path('craete_category/', CreateCategory.as_view(), name="project.createCategory"),
    path('craete_campaign/',CreateCampaign.as_view(), name="project.createCampaign"),
    path('details/<int:campaign_id>', campaign_details , name="campaign.details"),
    path('home/', home, name = 'project.home'),
    path('featured/', featured, name="project.featured"),
    path('latest/', latest, name="project.latest"),
    path('searchResults/', search, name="project.search"),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('nosearchResults/', search, name="project.nosearchresults"),
    #
    path('profile/', profile, name="project.profile"),

    ]

