from datetime import datetime

from django import forms
from project.models import Campaign, Category,Comment,Reply,Rate,Report,Donation,Comment_Report



from django import forms

from project.models import Campaign, Category

class CreateCampaignForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Title",
                "class": "form-control"
            }
        ))
    detail = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Details",
                "class": "form-control",
                'rows': '3'
            }
        ))
    total_target = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Total Target",
                "class": "form-control",
                "type": "number"
            }
        ))
    start_date = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Start date & time',
                'type': 'date',
                'class': 'form-control'
            }
        ))

    end_date = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'End date & time',
                'type': 'date',
                'class': 'form-control'
            }
        ))
    class Meta:
        model = Campaign
        fields = ['title', 'detail', 'total_target', 'tags', 'start_date', 'end_date', 'category', 'featured', 'image']

        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get("start_date")
            end_date = cleaned_data.get("end_date")
            today_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

            if today_date.date() > end_date.date():
                msg = "End date should be greater than Current date [ Should be after today !]."
                self._errors["end_time"] = self.error_class([msg])
            else:
                if end_date <= start_date:
                    msg = "End date should be greater than start date."
                    self._errors["end_time"] = self.error_class([msg])

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {}
# class CreateTagForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = '__all__'
#         widgets = {}

# class CustomizedImageCreationForm(forms.ModelForm):
#
#     class Meta:
#         model = Image
#
#         fields = '__all__'



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