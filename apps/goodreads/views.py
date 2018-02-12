import requests
from xml.etree import ElementTree
from xml.parsers.expat import ExpatError


from django.utils import six
from allauth.socialaccount import app_settings
from .provider import GoodreadsProvider
from allauth.socialaccount.providers.oauth.client import OAuth
from allauth.socialaccount.providers.oauth.views import (
    OAuthAdapter,
    OAuthCallbackView,
    OAuthLoginView,
)

class GoodreadsAPI(OAuth):
    url = "https://www.goodreads.com/user/show/{uid}.xml"
    auth_url = "https://www.goodreads.com/api/auth_user"

    def get_user_info(self):
        raw_xml = self.query(self.auth_url)
        if not six.PY3:
            raw_xml = raw_xml.encode("utf8")
        uid = ElementTree.fromstring(raw_xml).getchildren()[1].get("id")
        raw_xml = self.query(self.url.format(uid=uid))
        if not six.PY3:
            raw_xml = raw_xml.encode('utf8')
        try:
            return self.to_dict(ElementTree.fromstring(raw_xml))
        except (ExpatError, KeyError, IndexError):
            return None

    def to_dict(self, xml):
        """
        Convert XML structure to dict recursively, repeated keys
        entries are returned as in list containers.
        """
        children = list(xml)
        if not children:
            return xml.text
        else:
            out = {}
            for node in list(xml):
                if node.tag in out:
                    if not isinstance(out[node.tag], list):
                        out[node.tag] = [out[node.tag]]
                    out[node.tag].append(self.to_dict(node))
                else:
                    out[node.tag] = self.to_dict(node)
            return out

class GoodreadsOAuthAdapter(OAuthAdapter):
    provider_id = GoodreadsProvider.id
    settings = app_settings.PROVIDERS.get(provider_id, {})

    web_url = "https://www.goodreads.com"
    request_token_url = '{0}/oauth/request_token'.format(web_url)
    access_token_url = '{0}/oauth/access_token'.format(web_url)
    authorize_url = '{0}/oauth/authorize'.format(web_url)
    #profile_url = '{0}/user'.format(api_url)
    #emails_url = '{0}/user/emails'.format(api_url)

    def complete_login(self, request, app, token, **kwargs):
        #params = {'access_token': token.token}
        #resp = requests.get(self.profile_url, params=params)
        #extra_data = resp.json()
        #if app_settings.QUERY_EMAIL and not extra_data.get('email'):
        #    extra_data['email'] = self.get_email(token)
        client = GoodreadsAPI(request, app.client_id, app.secret,
                    self.request_token_url)
        extra_data = client.get_user_info()
        return self.get_provider().sociallogin_from_response(
            request, extra_data
        )

    def get_email(self, token):
        email = None
        params = {'access_token': token.token}
        resp = requests.get(self.emails_url, params=params)
        emails = resp.json()
        if resp.status_code == 200 and emails:
            email = emails[0]
            primary_emails = [
                e for e in emails
                if not isinstance(e, dict) or e.get('primary')
            ]
            if primary_emails:
                email = primary_emails[0]
            if isinstance(email, dict):
                email = email.get('email', '')
        return email


oauth2_login = OAuthLoginView.adapter_view(GoodreadsOAuthAdapter)
oauth2_callback = OAuthCallbackView.adapter_view(GoodreadsOAuthAdapter)
