"""urlconf for the base application"""

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import ( home, ProfileCreate, ProfileUpdate, ProfileDetail, 
        search_book_title, search_author_name, check_profile )
from .views import make_payment, payment_redirect, payment_webhook, ItemList
from .views import BoxDetail, BoxCreate, PaymentFulfillmentList

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^about/$', TemplateView.as_view(template_name="base/about.html"), name="about"),
    url(r'^profile/check/$', check_profile, name='profile-check'),
    url(r'^profile/view/(?P<pk>[^/]+)$', ProfileDetail.as_view(), name='profile-detail'),
    url(r'^profile/add/$', ProfileCreate.as_view(), name='profile-create'),
    url(r'^profile/edit/$', ProfileUpdate.as_view(), name='profile-edit'),
    url(r'^api/books/$', search_book_title, name='search-book'),
    url(r'^api/authors/$', search_author_name, name='search-author'),
    url(r'^payment/create/(?P<pk>[^/]+)$', make_payment, name='payment-create'),
    url(r'^payment/redirect/(?P<pk>[^/]+)$', payment_redirect, name='payment-redirect'),
    url(r'^payment/webhook/$', payment_webhook, name='payment-webhook'),
    url(r'^shop/$', ItemList.as_view(), name='shop'),
    url(r'^privacy/$', TemplateView.as_view(template_name="base/privacy.html"), name="privacy"),
    url(r'^tos/$', TemplateView.as_view(template_name="base/tos.html"), name="tos"),
    url(r'^box/review/(?P<pk>[^/]+)$', BoxDetail.as_view(), name="box-review"),
    url(r'^box/create/(?P<pk>[^/]+)$', BoxCreate.as_view(), name="box-create"),
    url(r'^payment/fulfillment/$', PaymentFulfillmentList.as_view(), name="payment-fulfillment"),
]
