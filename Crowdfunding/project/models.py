from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}'

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.name}'


class Campaign(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField(max_length=5000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    featured = models.BooleanField()
    tags = models.ManyToManyField(Tag, blank=True)
    # when maged add user i will add relation between project and user
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    image = models.ImageField(upload_to='project/images/', null=True, blank=True )
    campaign = models.ForeignKey(Campaign, default=None, on_delete=models.CASCADE, related_name="images")


class Comment(models.Model):
    comment = models.CharField(max_length=400, null=True)
    campaign = models.ForeignKey(Campaign, default=None, on_delete=models.CASCADE, related_name="comments")
    ##relation to user many to one
    created_at = models.DateTimeField(auto_now_add=True)
