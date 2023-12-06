from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'tags', 'file']
        widgets = {
            'content': CKEditorWidget(),
        }
