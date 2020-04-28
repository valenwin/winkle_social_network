from urllib import request

from django import forms
from django.core.files.base import ContentFile

from .models import Image, Comment

from account.utils import custom_slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

        widgets = {
            'url': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control mt-2 mb-2', 'placeholder': 'Type your description here...'})
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match '
                                        'valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = f"{custom_slugify(image.title)} {image_url.rsplit('.', 1)[1].lower()}"
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control mt-2',
                                          'placeholder': 'Type your comment here...', 'rows': '3'}),
        }
