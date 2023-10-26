from django.urls import path
from project.views import home, CreateImage, ImageView
# from project.views import CreateCampaign

urlpatterns = [
    # path('create/', CreateCampaign.as_view(), name="project.create"),
    path('home/', home, name = 'project.home'),
    path('uploadImage/', CreateImage.as_view(), name='images.create'),
    path('viewImage/', ImageView.as_view(), name='images.show'),
]
