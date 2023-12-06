from django.contrib import admin

# Register your models here.
#register articles model
from .models import Article
admin.site.register(Article)
