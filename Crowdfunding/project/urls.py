from django.urls import path
# from project.views import CreateCampaign
from project.views import profile

urlpatterns = [
    # path('create/', CreateCampaign.as_view(), name="project.create"),
      path('profile/', profile, name="project.profile"),

]
