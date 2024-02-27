from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "categories", "tags"]
        


class CommentForm(forms.Form):
    reply = forms.CharField(widget=CKEditorWidget())
    
