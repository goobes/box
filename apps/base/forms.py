
from django import forms
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from .models import Profile, Book, Author, Box, Publisher

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
    tracking_code = forms.CharField(required=False)

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'title', 'ol_id', 'isbn', 'genres', 'authors', 'publisher', 'year_of_publication'
            )
        widgets = {
            'authors': ModelSelect2MultipleWidget(
                queryset=Author.objects.all(),
                search_fields=['name__icontains'],
                attrs={'data-placeholder': 'Search for Author name', 'data-width': '20em' }
            ),
            'publisher': ModelSelect2Widget(
                queryset=Publisher.objects.all(),
                search_fields=['name__icontains'],
                attrs={'data-placeholder': 'Search for Publisher name', 'data-width': '20em'} 
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['authors'].required = False
        self.fields['publisher'].required = False
