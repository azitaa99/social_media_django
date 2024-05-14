from django import forms
from .models import Post, Comment
from django.forms import ModelForm




class PostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields=('body',)
        

class updatepostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields=('body',)

class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields=('body',)
        widgets={
            'body':forms.Textarea(attrs={'cols':30,'rows':5})
        }
        labels={
            'body':'your comment'
        }
    
class ReplyForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields=('body',)
        widgets={
            'body':forms.Textarea(attrs={'cols':30,'rows':2})
        }
        labels={
            'body':'reply'
        }
    

class postserachForm(forms.Form):
    search=forms.CharField()
        


        