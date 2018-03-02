"""Views for the base app"""

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from instamojo_wrapper import Instamojo
from datetime import datetime, timedelta
import logging
import hmac
import hashlib
from allauth.socialaccount.models import SocialAccount

from .models import Genre, Author, Publisher, Book, Profile, Item, Payment, Box
from .forms import ProfileForm, BoxForm, BookForm
from utils import has_profile

EMAIL_PAYMENT_RECEIVED = """
Hi {username},
You will be receiving your box shortly, do let us know how you like our selection of books.

Please feel free to contact us at goobesbookrepublic@gmail.com if you need any clarifications.

Team Goobe's Subscription Box
"""

logger = logging.getLogger(__name__)

User = get_user_model()

if settings.INSTAMOJO['TEST']:
    payment_api = Instamojo(api_key=settings.INSTAMOJO['API_KEY'],
        auth_token=settings.INSTAMOJO['AUTH_TOKEN'],
        endpoint='https://test.instamojo.com/api/1.1/')
else:
    payment_api = Instamojo(api_key=settings.INSTAMOJO['API_KEY'],
        auth_token=settings.INSTAMOJO['AUTH_TOKEN'])

def home(request):
    """ Default view for the root """
    items = Item.objects.order_by("pk").all()
    return render(request, 'base/home.html', context={'items': items})

def check_profile(request):
    if Profile.objects.filter(user__username=request.user):
        return redirect('home')
    else:
        return redirect('profile-create')

def search_book_title(request):
    data = serializers.serialize("json", Book.objects.filter(title__icontains=request.GET.get("q")))
    return JsonResponse(data, safe=False)

def search_author_name(request):
    data = serializers.serialize("json", Author.objects.filter(name__icontains=request.GET.get("name")))
    return JsonResponse(data, safe=False)

@login_required
def make_payment(request, pk):
    item = Item.objects.get(pk=pk)
    payment = Payment.objects.create(
            user=request.user,
            item=item,
            payment_date=datetime.today(),
            amount=item.price)
    if settings.DEBUG:
        response = payment_api.payment_request_create(
            amount=item.price,
            purpose=item.name,
            send_email=True,
            email=request.user.email,
            redirect_url=request.build_absolute_uri(reverse('payment-redirect', kwargs={'pk': payment.id}))
            )
    else:
        response = payment_api.payment_request_create(
            amount=item.price,
            purpose=item.name,
            send_email=True,
            email=request.user.email,
            redirect_url=request.build_absolute_uri(reverse('payment-redirect', kwargs={'pk': payment.id})),
            webhook=request.build_absolute_uri(reverse('payment-webhook'))
            )

    if response['success']:
        payment.payment_request_id = response['payment_request']['id']
        payment.save()
    else:
        logger.error("make_payment: payment gateway failed: %s" % response['message'])
    return render(request, 'base/payment_create.html',
                    {
                    'item': item,
                    'payment': payment,
                    'response': response
                    }
                )

@login_required
def payment_redirect(request, pk):
    payment = Payment.objects.get(pk=pk)
    payment.payment_id = request.GET.get("payment_id")
    payment.payment_request_id = request.GET.get("payment_request_id")
    payment.save()

    logger.info("payment_redirect: payment_id - {}".format(payment.payment_id))
    logger.info("payment_redirect: payment_request_id - {}".format(payment.payment_request_id))
    return render(request, 'base/payment_complete.html')

@csrf_exempt
def payment_webhook(request):
    data = request.POST.dict()
    mac = data.pop("mac")
    message = "|".join(v for k, v in sorted(data.items(), key=lambda x: x[0].lower()))
    mac_calculated = hmac.new(settings.INSTAMOJO['SALT'].encode(), message.encode(), hashlib.sha1).hexdigest()
    logger.info("payment_webhook: mac - {}".format(mac))
    logger.info("payment_webhook: calculated mac - {}".format(mac_calculated))
    if mac_calculated == mac:
        payment = Payment.objects.get(payment_request_id=data['payment_request_id'])
        payment.payment_id = data['payment_id']
        payment.payment_request_id = data['payment_request_id']
        payment.status = data['status']
        payment.fees = data['fees']
        payment.longurl = data['longurl']
        payment.shorturl = data['shorturl']

        if payment.status == 'Credit':
            payment.user.profile.boxes_remaining = payment.user.profile.boxes_remaining + payment.item.boxes_added
            payment.user.profile.save()
            send_mail(
                'Payment received for: {}'.format(payment.item.name),
                EMAIL_PAYMENT_RECEIVED.format(username=payment.user.username),
                "no-reply@box.goobes.in",
                [payment.user.email],
                fail_silently=False
            )
        payment.save()
        return HttpResponse(status_code=200)
    else:
        logger.error("webhook failed mac calculation")
        return HttpResponse(status_code=400)

class ProfileCreate(CreateView):
    model = Profile
    form_class = ProfileForm

    def dispatch(self, request, *args, **kwargs):
        if has_profile(request.user):
            return HttpResponseRedirect(reverse('profile-edit'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        for book_id in self.request.POST.getlist('favourite_books'):
            book = Book.objects.get(pk=int(book_id))
            form.instance.favourite_books.add(book)

        for author_id in self.request.POST.getlist('favourite_authors'):
            author = Author.objects.get(pk=int(author_id))
            form.instance.favourite_authors.add(author)
        return response

class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class ProfileDetail(DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goodreads'] = SocialAccount.objects.filter(provider='goodreads', user=self.object.user).first()
        return context

class ItemList(ListView):
    model = Item

    ordering = ['pk']

class BoxDetail(DetailView):
    model = Box

class SuperUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class StaffUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class BoxCreate(StaffUserMixin, FormView):
    model = Box
    form_class = BoxForm
    template_name = "base/box_create.html"

    def get_success_url(self):
        return reverse("payment-fulfillment")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment'] = Payment.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        payment = Payment.objects.get(pk=self.kwargs['pk'])
        box = Box(payment=payment)
        if form.cleaned_data['shipped']:
            box.shipped_at = datetime.now()
        box.save()
        box.books.set(form.cleaned_data['books'])
        if payment.box_set.count() >= payment.item.boxes_added:
            payment.fulfilled = True
            payment.save()
        return super().form_valid(form)

class PaymentFulfillmentList(StaffUserMixin, ListView):
    queryset = Payment.objects.filter(status='Credit', fulfilled=False)

class BookCreate(StaffUserMixin, CreateView):
    model = Book
    form_class = BookForm

    def get_success_url(self):
        if self.request.POST.get("_addanother"):
            return reverse("book-create")
        else:
            return reverse("home")

    def form_valid(self, form):
        form.instance.publisher, created = Publisher.objects.get_or_create(name=self.request.POST.get("publisher_auto"))
        response = super().form_valid(form)
        for author in self.request.POST.getlist("author_auto"):
            ol_id = author.split("/")[-1]
            form.instance.authors.add(Author.objects.get(ol_id=ol_id))

        return response
