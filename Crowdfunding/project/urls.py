from django.urls import path
from project.views import home, CreateImage, ImageView, featured, latest, search, CategoryDetailView
from project.views import ListAllCampaign, CreateCampaign, CreateTag, CreateCategory, ListAllCategories

urlpatterns = [
    path('list_all/', ListAllCampaign.as_view(), name="project.list.all.campaign"),
    path('craete_tag/', CreateTag.as_view(), name="project.createTag"),
    path('craete_category/', CreateCategory.as_view(), name="project.createCategory"),
    path('craete_campaign/',CreateCampaign.as_view(), name="project.createCampaign"),
    path('home/', home, name = 'project.home'),
    path('uploadImage/', CreateImage.as_view(), name='images.create'),
    path('viewImage/', ImageView.as_view(), name='images.show'),
    path('featured/', featured, name="project.featured"),
    path('latest/', latest, name="project.latest"),
    path('searchResults/', search, name="project.search"),
    path('categoriesDetails/',ListAllCategories.as_view(), name="project.listCategory"),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('nosearchResults/', search, name="project.nosearchresults"),

    
    ]
