
from django import forms
from django_select2.forms import ModelSelect2MultipleWidget
from .models import Profile, Book, Author, Box

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
                'address', 'city', 'state', 'postal_code', 'phone_mobile', 'phone_landline', 
                'genres', 'interests'
                )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 24}),
            'genres': forms.CheckboxSelectMultiple(),
            'interests': forms.Textarea(attrs={'rows': 5, 'cols': 48})
        }

class BoxForm(forms.Form):
    shipped = forms.BooleanField(required=False)
    books = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        queryset=Book.objects.all(),
        search_fields=['title__icontains'],
        attrs={'data-placeholder': 'Search for Book titles', 'data-width': '20em' }
        ), queryset=Book.objects.all(), required=True)
