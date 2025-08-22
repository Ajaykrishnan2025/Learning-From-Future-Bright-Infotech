from django.db import models

# Create your models here.
class Post(models.Model):
    tittle = models.CharField(max_length=100)
    content = models.TextField()
    img_url = models.URLField(null=True)


 
