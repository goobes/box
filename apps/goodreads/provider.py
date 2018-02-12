from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class GoodreadsAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('profile')

    def get_avatar_url(self):
        return self.account.extra_data.get('image_url')

    def to_str(self):
        dflt = super(GoodreadsAccount, self).to_str()
        return next(
            value
            for value in (
                self.account.extra_data.get('name', None),
                self.account.extra_data.get('login', None),
                dflt
            )
            if value is not None
        )


class GoodreadsProvider(OAuth2Provider):
    id = 'goodreads'
    name = 'Goodreads'
    account_class = GoodreadsAccount

    def get_auth_url(self, request, action):
        return "https://www.goodreads.com/oauth/authorize"

    def get_default_scope(self):
        scope = []
        if app_settings.QUERY_EMAIL:
            scope.append('user:email')
        return scope

    def extract_uid(self, data):
        return str(data['user']['id'])

    def extract_common_fields(self, data):
        return dict(
                about=data['user'].get('about'),
                age=data['user'].get('age'),
                image_url=data['user'].get('image_url'),
                gender=data['user'].get('gender'),
                profile=data['user'].get('link')
                )

provider_classes = [GoodreadsProvider]
