from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator


# Create your models here.




class User(models.Model):
    pass


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




class Donation (models.Model):
    donation = models.DecimalField(max_digits=10,
                                    decimal_places=2 ,
                                   validators=[MinValueValidator(limit_value=5.00)],
                                   default=5.00)
    project = models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name="donation")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="donation")
    created_at = models.DateTimeField(auto_now_add=True)




class Report (models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="reports")
    project = models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name="reports")
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
    report_comment=models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):
    rate = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ])
    projcet = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="rate")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="rate")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reply(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reply = models.CharField(max_length=100)
    # comment = models.ForeignKey()
    # user = models.ForeignKey()

