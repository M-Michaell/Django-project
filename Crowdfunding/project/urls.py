from django.urls import path
from project.views import ListAllCampaign, CreateCampaign, CreateTag, CreateCategory

urlpatterns = [
    path('list_all/', ListAllCampaign.as_view(), name="project.list.all.campaign"),
    path('craete_tag/', CreateTag.as_view(), name="project.createTag"),
    path('craete_category/', CreateCategory.as_view(), name="project.createCategory"),
    path('craete_campaign/',CreateCampaign.as_view(), name="project.createCampaign"),
]
