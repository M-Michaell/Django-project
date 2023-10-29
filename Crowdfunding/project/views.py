from django.core.exceptions import ValidationError
from django.shortcuts import render ,redirect
from django.template import loader
from django.urls import reverse_lazy ,reverse
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from decimal import Decimal
from django.contrib.auth import authenticate, login


from django.db.models import Sum, Count,Avg
from django.views.generic import ListView ,DetailView
from project.form import CreateCampaignForm, CreateCategoryForm ,CreateDonationForm,CreateCommentForm,CreateRatingForm, CreateReportForm,CreateCommentReportForm,PasswordConfirmationForm
from project.models import Campaign, Category,Comment,Reply,Rate,Report,Donation,Comment_Report
from django.contrib.auth.models import  User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from account.models import CustomUser
from django.contrib.messages import add_message, constants as messages



# Create your views here.
class ListAllCampaign(ListView):
    model = Campaign
    template_name = 'project/list_all_campaign.html'
    context_object_name = 'campaigns'

class CreateCampaign(CreateView):
    model = Campaign
    template_name = 'project/create_campaign.html'
    form_class = CreateCampaignForm
    success_url = reverse_lazy('project.upload')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class DeleteCampaign(DeleteView):
    model = Campaign
    template_name = 'project/delete.html'
    context_object_name = "campaign"
    success_url = reverse_lazy('project.list.all.campaign')

class EditCampaign(UpdateView):
    model = Campaign
    template_name = 'project/edit_campaign.html'
    context_object_name = "campaign"
    form_class = CreateCampaignForm
    success_url = reverse_lazy('project.list.all.campaign')

class CreateCategory(CreateView):
    model = Category
    template_name = 'project/create_category.html'
    form_class = CreateCategoryForm
    success_url = reverse_lazy('project.home')


def getUser(request):
        active_user_id = CustomUser.objects.get(id=request.session['user_id'])
        return active_user_id


@login_required(login_url='/account/login/') 
def campaign_details(request, campaign_id):
    try:
        campaign = Campaign.objects.get(pk=campaign_id)
    except Campaign.DoesNotExist:
        raise Http404("Campaign does not exist")

    total_donation = campaign.donation.aggregate(total_donation=Sum('donation'))['total_donation'] or 0.00
    donation_count = campaign.donation.aggregate(donation_count=Count('id'))['donation_count']
    comments = campaign.comments.all()
    tags = campaign.tags.all()
    images_all = campaign.images.all()
    rating = round(campaign.rate.aggregate(rate=Avg('rate'))['rate'] or 0.00 ,2)
    related_campaigns = Campaign.objects.filter(tags__in=tags).exclude(pk=campaign_id).distinct()[:4]
    progress = (float(total_donation) / float(campaign.total_target)) * 100

    # active_user_id=getUser(request)
    if Donation.objects.filter(campaign=campaign).last() :
        last_donation = Donation.objects.filter(campaign=campaign).last().created_at
    else:
        last_donation="no donations yet"
    can_cancel=False
    if progress < 25:
        can_cancel=True
    

    # Initialize your forms
    comment_form = CreateCommentForm()
    donation_form = CreateDonationForm()
    report_form = CreateReportForm()
    comment_report_form =CreateCommentReportForm()
    create_rate =CreateRatingForm()
    password_form = PasswordConfirmationForm()

    error_message = None
    context = {
    'campaign': campaign,
    'total_donation': total_donation,
    'donation_count': donation_count,
    'comments': comments,
    'tags': tags,
    'rating_width': rating * 20,
    'f_image': images_all[0],
    'images': images_all[1:],
    'related_campaigns': related_campaigns,
    "progress": progress,
    'comment_form': comment_form,
    'donation_form': donation_form,
    'report_form': report_form,
    "comment_report_form":comment_report_form,
    'last_donation': last_donation,
    "create_rate":create_rate,
    "rating" :rating,
    "error_message": error_message,
    "request": request,
    'password_form': password_form,
    'can_cancel':can_cancel
    
    # "active_user_id":active_user_id,

}

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CreateCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.campaign = campaign
                comment.user = request.user
                comment.save()
                add_message(request, messages.SUCCESS, "Your comment has been successfully added.")
                return redirect('campaign.details', campaign_id=campaign_id)

        elif 'donation_submit' in request.POST:
            donation_form = CreateDonationForm(request.POST)
            if donation_form.is_valid():
                donation = donation_form.save(commit=False)
                donation.campaign = campaign
                donation.user = request.user
                donation.save()
                add_message(request, messages.SUCCESS, "Your donation has been successfully processed, Tkanks 🙏")
                return redirect('campaign.details', campaign_id=campaign_id)
            else:
                add_message(request, messages.ERROR, "Your donation should be geater than 5.")
                return redirect('campaign.details', campaign_id=campaign_id)

            
        elif 'report_submit' in request.POST:
            report_form = CreateReportForm(request.POST)
            if report_form.is_valid():
                report = report_form.save(commit=False)
                report.campaign = campaign
                report.user = request.user
                report.save()
                add_message(request, messages.SUCCESS, "Your report has been successfully submitted.")
                return redirect('campaign.details', campaign_id=campaign_id)
            
        elif 'comment_report' in request.POST:
            comment_report_form = CreateCommentReportForm(request.POST)
            if comment_report_form.is_valid():
                comment_id = request.POST['comment_id']  
                report = comment_report_form.save(commit=False)
                report.comment = Comment.objects.get(id=comment_id)
                report.user = request.user
                report.save()
                add_message(request, messages.SUCCESS, "Your comment report has been successfully submitted.")
                return redirect('campaign.details', campaign_id=campaign_id)
            

        elif 'rate_submit' in request.POST:
            create_rate = CreateRatingForm(request.POST)
            if create_rate.is_valid():
                user_rating = Rate.objects.filter(campaign=campaign, user=request.user).first()

                if user_rating:
                    add_message(request, messages.ERROR, "You have already rated this campaign before.")
                else:
                    rate = create_rate.save(commit=False)
                    rate.user = request.user
                    rate.campaign = campaign
                    rate.save()
                    add_message(request, messages.SUCCESS, "Your rating has been successfully added.")
                    return redirect('campaign.details', campaign_id=campaign_id)
                

            
        elif 'cancel' in request.POST:
            password_form = PasswordConfirmationForm(request.POST)
            entered_password = request.POST.get('password', '')
            user = request.user  # Get the current user

            if user.check_password(entered_password):
                # Password matches, delete the campaign
                campaign.delete()
                return redirect(reverse("project.home"))
            else:
                add_message(request, messages.ERROR, "password is incorrect")
                return redirect('campaign.details', campaign_id=campaign_id)




    return render(request, 'project/details.html', context=context)









class CreateDonation(CreateView):
    model = Donation
    template_name = 'project/create_donation.html'
    form_class = CreateDonationForm
    success_url = reverse_lazy('campaign.details',id='campaign_id')
    def get_success_url(self):
        return reverse('campaign.details', kwargs={'campaign_id': self.kwargs['campaign_id']})








def home(request):
    return render(request, 'project/home.html')



def home(request):
    featured = Campaign.objects.filter(featured=True).order_by('-created_at')[:5]
    latest = Campaign.objects.all().order_by('-created_at')[:5]
    return render(request, 'project/home.html', context = {"featured": featured, "latest": latest})


def featured(request):
    featured = Campaign.objects.filter(featured=True).order_by('-created_at')[:5]
    return render(request, 'project/featured.html', context = {"featured": featured})

def latest(request):
        latest = Campaign.objects.all().order_by('-created_at')[:5]
        return render(request, 'project/latest.html', context = {"latest": latest})


def search(request):
  q = request.GET.get("q", "")
  campaignList = Campaign.objects.filter(
      Q(title__icontains=q) | Q(tags__name__icontains=q)
  )

  if not campaignList:
    # Redirect to a page with no search results found
    return render(request, "project/no_search_results.html")


  return render(request, "project/search.html", context={"campaignList": campaignList})

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'project/category_detail.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['campaigns'] = Campaign.objects.filter(category__id=self.object.id)
            return context

#test image-------------------------------------------------------------------
from django.views.generic.edit import FormView
from project.form import UploadForm
from project.models import Attachment

class UploadView(FormView):
    template_name = 'project/create.html'
    form_class = UploadForm
    success_url = reverse_lazy('project.list.all.campaign ')

    def post(self, request):
        data = request.POST
        print('mohmmed', data)
        campaign = Campaign.objects.get(id=data['campaign'])
        images = request.FILES.getlist('attachments')
        for image in images:
            photo = Attachment.objects.create(
                image=image,
                campaign=campaign
            )
        return redirect(reverse('project.list.all.campaign'))






def profile(request):
    user_id = request.user.id
    user_donation = Donation.objects.filter(user_id=user_id)
    user_campaign = Campaign.objects.filter(user_id=user_id)
    return render(request, template_name='project/profile.html', 
    context = {
    'user_donation': user_donation,
    'user_campaign': user_campaign})