from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.fields['title'].initial = 'Default title'
    #     self.fields['content'].initial = 'Default content'

    class Meta:
        model = Post
        fields = ["title", "content", "categories", "tags"]

        


class CommentForm(forms.Form):
    reply = forms.CharField(widget=CKEditorWidget())
    

