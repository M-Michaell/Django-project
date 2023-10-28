from django.shortcuts import render ,redirect 
from django.template import loader
from django.urls import reverse_lazy ,reverse
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db.models import Sum, Count,Avg
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView ,DetailView
from project.form import CreateCampaignForm, CreateCategoryForm, CreateTagForm , CustomizedImageCreationForm ,CreateDonationForm,CreateCommentForm,CreateRatingForm, CreateReportForm,CreateCommentReportForm
from project.models import Campaign, Category,Comment,Reply,Rate,Report,Donation,Tag,Image,Comment_Report



#
# # Create your views here.
class ListAllCampaign(ListView):
    model = Campaign
    template_name = 'project/list_all_campaign.html'
    context_object_name = 'campaigns'


class CreateCampaign(CreateView):
    model = Campaign
    template_name = 'project/create_campaign.html'
    form_class = CreateCampaignForm
    success_url = reverse_lazy('project.list.all.campaign')

class CreateCategory(CreateView):
    model = Category
    template_name = 'project/create_category.html'
    form_class = CreateCategoryForm
    success_url = reverse_lazy('project.createTag')

class CreateTag(CreateView):
    model = Tag
    template_name = 'project/create_tag.html'
    form_class = CreateTagForm
    success_url = reverse_lazy('project.createCampaign')

    def form_valid(self, form):
        # Determine which button was clicked
        if 'save_button' in self.request.POST:
            self.success_url = reverse_lazy('project.createCampaign')
        elif 'other_button' in self.request.POST:
            self.success_url = reverse_lazy('project.createTag')

        return super().form_valid(form)


from django.contrib.messages import add_message, constants as messages
# def getUser(request):
#         user = Register.objects.get(id=request.session['user_id'])
#         return user
def campaign_details(request, campaign_id):
    try:
        campaign = Campaign.objects.get(pk=campaign_id)
    except Campaign.DoesNotExist:
        raise Http404("Campaign does not exist")

    total_donation = campaign.donation.aggregate(total_donation=Sum('donation'))['total_donation'] or 0.00
    donation_count = campaign.donation.aggregate(donation_count=Count('id'))['donation_count']
    comments = campaign.comments.all()
    tags = campaign.tags.all()
    images_all = campaign.image.all()
    rating = round(campaign.rate.aggregate(rate=Avg('rate'))['rate'] or 0.00 ,2)
    related_campaigns = Campaign.objects.filter(tags__in=tags).exclude(pk=campaign_id).distinct()[:4]
    progress = (float(total_donation) / float(campaign.total_target)) * 100
    if Donation.objects.filter(campaign=campaign).last() :
        last_donation = Donation.objects.filter(campaign=campaign).last().created_at
    else:
        last_donation="no donations yet"
    

    # Initialize your forms
    comment_form = CreateCommentForm()
    donation_form = CreateDonationForm()
    report_form = CreateReportForm()
    comment_report_form =CreateCommentReportForm()
    create_rate =CreateRatingForm()

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
                add_message(request, messages.SUCCESS, "Your donation has been successfully processed.")
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

class CreateImage(CreateView):
    model = Image
    template_name = 'project/create.html'
    form_class = CustomizedImageCreationForm
    success_url = reverse_lazy("project.home")

    def form_valid(self, form):
        # Determine which button was clicked
        if 'save' in self.request.POST:
            self.success_url = reverse_lazy('project.home')
        elif 'add' in self.request.POST:
            self.success_url = reverse_lazy('images.create')

        return super().form_valid(form)


class DeleteImage(DeleteView):
    model = Image
    template_name = 'accounts/delete.html'
    success_url = reverse_lazy('project.home')

class EditProfileView(UpdateView):
   model = Image
   template_name = 'project/edit.html'
   form_class = CustomizedImageCreationForm
   success_url = reverse_lazy('project.home')

class ImageView(DetailView):
    model = Image
    template_name = 'project/view.html'
    context_object_name = 'image'
    def get_object(self, queryset=None):
        return self.request.user
    

    

