
from django import forms
from .models import Profile, Book, Author

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
