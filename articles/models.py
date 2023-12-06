from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='article_files/', null=True, blank=True)


    def __str__(self):
        return self.title

