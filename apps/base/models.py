"""Base models"""

from django.db import models
from django.conf import settings
from django.urls import reverse

STATES = (
    (u'AP', u'ANDHRA PRADESH'),
    (u'AR', u'ARUNACHAL PRADESH'),
    (u'AS', u'ASSAM'),
    (u'BR', u'BIHAR'),
    (u'CG', u'CHATTISGARH'),
    (u'DL', u'DELHI'),
    (u'GA', u'GOA'),
    (u'GJ', u'GUJARAT'),
    (u'HR', u'HARYANA'),
    (u'HP', u'HIMACHAL PRADESH'),
    (u'JK', u'JAMMU & KASHMIR'),
    (u'JS', u'JHARKHAND'),
    (u'KA', u'KARNATAKA'),
    (u'MP', u'MADHYA PRADESH'),
    (u'MH', u'MAHARASHTRA'),
    (u'MN', u'MANIPUR'),
    (u'ML', u'MEGHALAYA'),
    (u'MZ', u'MIZORAM'),
    (u'NL', u'NAGALAND'),
    (u'OR', u'ORISSA'),
    (u'PB', u'PUNJAB'),
    (u'RJ', u'RAJASTHAN'),
    (u'SK', u'SIKKIM'),
    (u'TN', u'TAMIL NADU'),
    (u'TR', u'TRIPURA'),
    (u'UK', u'UTTARAKHAND'),
    (u'UP', u'UTTAR PRADESH'),
    (u'WB', u'WEST BENGAL'),
    (u'AN', u'ANDAMAN & NICOBAR'),
    (u'CH', u'CHANDIGARH'),
    (u'DN', u'DADAR & NAGAR HAVELI'),
    (u'DD', u'DAMAN & DIU'),
    (u'LD', u'LAKSHADWEEP'),
    (u'PY', u'PONDICHERRY')
)


class Genre(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=64, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return "<Publisher: %s>" % self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    ol_id = models.CharField(max_length=16, unique=True)
    alternate_names = models.CharField(max_length=512, blank=True)
    year_of_birth = models.CharField(max_length=10)
    year_of_death = models.CharField(max_length=10)

    def __str__(self):
        return "<Author: %s>" % self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    ol_id = models.CharField(max_length=16, unique=True)
    isbn = models.CharField(max_length=20)
    genres = models.ManyToManyField(Genre)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    year_of_publication = models.CharField(max_length=10)

    def __str__(self):
        return "<Book: %s>" % self.title

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, choices=STATES)
    postal_code = models.CharField(max_length=8)
    phone_mobile = models.CharField(max_length=13)
    phone_landline = models.CharField(max_length=20, blank=True)
    genres = models.ManyToManyField(Genre)
    favourite_books = models.ManyToManyField(Book, blank=True)
    favourite_authors = models.ManyToManyField(Author, blank=True)
    paid_till = models.DateField(null=True, blank=True)

    def __str__(self):
        return "<Profile: %s>" % self.user

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'pk': self.id})

class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=255)
    #maximum price of 99999.99
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to="items", blank=True)
    boxes_added = models.IntegerField()

    def __str__(self):
        return "<Item: %s-%d>" % (self.name, self.price)

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    payment_date = models.DateField()
    payment_id = models.CharField(max_length=64)
    payment_request_id = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    fees = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    longurl = models.URLField()
    shorturl = models.URLField()
    status = models.CharField(max_length=16)
