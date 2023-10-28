from django import forms
from project.models import Campaign, Category,Comment,Reply,Rate,Report,Donation,Tag,Image,Comment_Report


from django import forms

from project.models import Campaign, Category, Tag, Image

class CreateCampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = '__all__'


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {}
class CreateTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {}

class CustomizedImageCreationForm(forms.ModelForm):

    class Meta:
        model = Image
        
        fields = '__all__'



class CreateReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('report', 'report_comment')
        widgets = {
            'report_comment': forms.Textarea(attrs={'class': 'form-control','rows':"2"}),
            'report':forms.Select(attrs={'class': 'form-control'})
        }

    # def clean_report_comment(self):
    #     data = self.cleaned_data['report_comment']

    #     if not data.is_valid():
    #         raise forms.ValidationError("Invalid data")
    #     return data


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('comment',)

class CreateRatingForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('rate',)
        widgets = {
            'rate':forms.Select(attrs={'class': 'form-control'})
        }
        
class CreateCommentReportForm(forms.ModelForm):
    class Meta:
        model=Comment_Report
        fields=('report',)
        widgets = {
            'report':forms.Select(attrs={'class': 'form-control'})
        }


        
class CreateReplyForm(forms.ModelForm):
    class Meta:
        model=Reply
        fields='__all__'

        
class CreateDonationForm(forms.ModelForm):
    class Meta:
        model=Donation
        fields=('donation',)