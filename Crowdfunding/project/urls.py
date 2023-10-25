from django.urls import path
from project.views import test

urlpatterns = [
    # path('create/', CreateCampaign.as_view(), name="project.create"),
    path('', test, name="create"),
]
