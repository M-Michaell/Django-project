from django.db import models
from account.models import CustomUser
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.shortcuts import reverse
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
from django.db.models import Sum, Count,Avg


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f'{self.name}'




class Campaign(models.Model):
    title = models.CharField(max_length=100, unique=True)
    detail = models.TextField(max_length=5000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    featured = models.BooleanField()
    image = models.ImageField(upload_to='project/images/')
    tags = TaggableManager()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None,related_name="campaign")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be greater than start date.")

    def __str__(self):
        return f'{self.title}'

    def get_image_url(self):
        return f'/media/{self.image}'

    def get_details(self):
        return reverse('campaign.details', args=[self.id])

    def get_edit_url(self):
        return reverse('project.editCampaign', args=[self.id])

    def get_delete(self):
        return reverse('campaign.delete', args=[self.id])
    
    def get_progress(self):
        total_donation = self.donation.aggregate(total_donation=Sum('donation'))['total_donation'] or 0.00
        progress = (float(total_donation) / float(self.total_target)) * 100
        return progress
    
    def get_total_deonation(self):
        total_donation = self.donation.aggregate(total_donation=Sum('donation'))['total_donation'] or 0.00
        return total_donation

    @classmethod
    def get_sepcific_object(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def get_all_campaign(cls):
        return cls.objects.all()


class Donation (models.Model):
    donation = models.DecimalField(max_digits=10,
                                    decimal_places=2 ,
                                   validators=[MinValueValidator(limit_value=5.00)],
                                   default=5.00)
    campaign = models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name="donation")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="donation")
    created_at = models.DateTimeField(auto_now_add=True)




class Report (models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="reports")
    campaign = models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name="reports")
    report_category =[("1","Flase Information"),
                  ("2","Violenece"),
                  ("3","Harassment"),
                  ("4","spam"),
                  ("5","Hate speech"),
                  ("6","Nudity"),
                  ("7","Terroism"),
                  ("8","Something else")
                  ]
    report=models.CharField(max_length=50,choices=report_category,default="1")
    report_comment=models.TextField(default='',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):

    RATE_CHOICES = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]

    rate = models.IntegerField(choices=RATE_CHOICES, default=1)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, related_name='rate')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rate')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} rated {self.campaign.title} with {self.rate} stars"



class Comment(models.Model):
    comment = models.CharField(max_length=400, null=True)
    campaign = models.ForeignKey(
        Campaign, default=None, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comment")
    
class Reply(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reply = models.CharField(max_length=100)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="reply")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reply")

class Comment_Report(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="comment_report")
    report_category=[("1","Flase Information"),
                  ("2","Violenece"),
                  ("3","Harassment"),
                  ("4","spam"),
                  ("5","Hate speech"),
                  ("7","Terroism"),
                  ("8","Something else")]
    report =  models.CharField(
        max_length=200,
        choices=report_category,
        default="1",
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_report"
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='comment_report')



#test image-------------------------------------------------------------------
class Attachment(models.Model):
    image = models.ImageField(upload_to='project/images',null=False, blank=False)
    campaign = models.ForeignKey(Campaign, default=None, on_delete=models.CASCADE, related_name="images")


    def __str__(self):
        return f'{self.campaign.title}'
    def get_image_url(self):
        return f'/media/{self.image}'