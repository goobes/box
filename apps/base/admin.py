
from django.contrib import admin
from .models import Genre, Publisher, Author, Book, Profile, Item, Payment

for m in [Genre, Publisher, Author, Book, Profile, Item, Payment]:
    admin.site.register(m)

