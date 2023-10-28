from django.db import models
from account.models import CustomUser
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.shortcuts import reverse
from taggit.managers import TaggableManager


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}'

# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#     def __str__(self):
#         return f'{self.name}'

# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#     def __str__(self):
#         return f'{self.name}'


class Campaign(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField(max_length=5000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    featured = models.BooleanField()
    image = models.ImageField(upload_to='project/images/', null=True, blank=True)
    tags = TaggableManager()
    #user = models.ForeignKey(User, on_delete=models.CASCADE, default=None,related_name="campaign")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None,related_name="campaign")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    def get_image_url(self):
        return f'/media/{self.image}'

    def get_show_url(self):
        return reverse('posts.details', args=[self.id])

    def get_edit_url(self):
        return reverse('posts.edit', args=[self.id])

    def get_delete_url(self):
        return reverse('posts.delete', args=[self.id])




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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rate')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} rated {self.campaign.title} with {self.rate} stars"

class Image(models.Model):
    image = models.ImageField(upload_to='project/images/', null=True, blank=True )
    campaign = models.ForeignKey(Campaign, default=None, on_delete=models.CASCADE, null=True, blank=True, related_name="image")

    
    def get_image_url(self):
        return f'/media/{self.image}'


class Comment(models.Model):
    comment = models.CharField(max_length=400, null=True)
    campaign = models.ForeignKey(Campaign, default=None, on_delete=models.CASCADE, related_name="comments")
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
        default='1',
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='comment_report')



