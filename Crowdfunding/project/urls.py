from django.urls import path
from project.views import campaign_details,CreateDonation
from project.views import DeleteCampaign, ListAllCampaign, EditCampaign ,CreateCampaign,  CreateCategory
from django.contrib.auth.decorators import login_required
from project.views import CreateCampaign,  CreateCategory, home, featured, latest, search, CategoryDetailView, profile, UploadView




urlpatterns = [
    path('craete_category/', CreateCategory.as_view(), name="project.createCategory"),
    path('craete_campaign/',CreateCampaign.as_view(), name="project.createCampaign"),
    path('details/<int:campaign_id>', campaign_details , name="campaign.details"),
    path('', home, name = 'project.home'),
    path('featured/', featured, name="project.featured"),
    path('latest/', latest, name="project.latest"),
    path('searchResults/', search, name="project.search"),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('nosearchResults/', search, name="project.nosearchresults"),
    path('profile/', profile, name="project.profile"),
    path('<int:pk>/delete', login_required(DeleteCampaign.as_view()), name="project.deleteCampaign"),
    path('<int:pk>/edit', login_required(EditCampaign.as_view()), name="project.editCampaign"),



    path('upload/', UploadView.as_view(), name="project.upload")

]

