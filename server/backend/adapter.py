import jwt
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group


class PeCoReTSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_roles(self, request, sociallogin):
        provider = self.get_provider(request, sociallogin.account.provider)
        user = sociallogin.user
        client_id = provider.app.client_id
        # token already verified previously
        token = jwt.decode(sociallogin.token.token, options={"verify_signature": False})
        if not token.get('resource_access', {}).get(client_id):
            # resource access not found in token - nothing to do here
            return
        roles = token['resource_access'][client_id].get('roles', [])
        # clear existing groups to be in sync with provider
        user.groups.clear()
        for role in roles:
            # get group for role
            try:
                group = Group.objects.get(name=role)
            except Group.DoesNotExist:
                continue
            user.groups.add(group)
        return user

    def pre_social_login(self, request, sociallogin):
        if hasattr(sociallogin.account, 'user'):
            # update roles when request is not first signup
            self.populate_roles(request, sociallogin)
        return super().pre_social_login(request, sociallogin)

    def save_user(self, request, sociallogin, form=None):
        # save users after first signup
        u = super().save_user(request, sociallogin, form)
        self.populate_roles(request, sociallogin)
        return u

    def is_open_for_signup(self, request, sociallogin):
        # prevent external signups but allow allauth to create new accounts
        if "/login/callback" in request.path:
            return True
        return True


class PeCoReTAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False
