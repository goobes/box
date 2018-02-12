
from django import forms
from .models import Profile, Book, Author

class ProfileForm(forms.ModelForm):
    #favourite_books = forms.ModelMultipleChoiceField(queryset=Book.objects.none(), required=False)
    #favourite_authors = forms.ModelMultipleChoiceField(queryset=Author.objects.none(), required=False)
    #favourite_books = forms.ModelMultipleChoiceField(required=False)
    #favourite_authors = forms.ModelMultipleChoiceField(required=False)
    #favourite_books = forms.MultipleChoiceField(required=False)
    #favourite_authors = forms.MultipleChoiceField(required=False)

    class Meta:
        model = Profile
        fields = (
                'address', 'city', 'state', 'postal_code', 'phone_mobile', 'phone_landline', 
                'genres', #'favourite_books', 'favourite_authors'
                )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 24}),
            'genres': forms.CheckboxSelectMultiple(),
        }
