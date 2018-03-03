from django.core.management.base import BaseCommand, CommandError
from base.models import Payment
from django.conf import settings
from instamojo_wrapper import Instamojo


class Command(BaseCommand):
    help = "Updates Payments from Instamojo for payments that have not been fully captured in our system"

    def handle(self, *args, **options):
        api = Instamojo(api_key=settings.INSTAMOJO['API_KEY'], auth_token=settings.INSTAMOJO['AUTH_TOKEN'])
        for payment in Payment.objects.filter(status=''):
            if payment.payment_request_id == '':
                continue
            response = api.payment_request_status(payment.payment_request_id)
            payment.status = response['payment_request']['status']
            payment.longurl = response['payment_request']['longurl']
            payment.shorturl = response['payment_request']['shorturl']
            if len(response['payment_request']['payments']) > 0:
                payresp = response['payment_request']['payments'][0]
                if payment.payment_id == '':
                    payment.payment_id = payresp['payment_id']
                payment.status = payresp['status']
                payment.fees = payresp['fees']

            payment.save()
