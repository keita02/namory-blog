from django import forms
# from tinymce import TinyMCE
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from .models import Post, Comment, Contact


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={'required': True, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'overview', 'content','post_image', 
        'categories', 'previous_post', 'next_post','featured' )


class CommentForm(forms.ModelForm):
    commentaire = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Votre commentaire...',
        'id': 'usercomment',
        'rows': '4'
    }))
    class Meta:
        model = Comment
        fields = ('commentaire', )


class ContactForm(forms.ModelForm):
    nom = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Votre nom',
        'class': 'form-control',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder': 'Laissez un commentaire',
        'rows': '10'
        }) )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields['nom'].widget.attrs['placeholder'] = 'Nom'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Contact
        fields = '__all__'