from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from authentications.models import *


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        try:
            email = sociallogin.account.extra_data.get("email")

            if User.objects.filter(email = email).exists():
                username = email.split("@")[0]

                account = Account.objects.get(username = username)

                sociallogin.account = SocialAccount.objects.get(user = account)

                sociallogin.connect(request, account)
                    
        except Account.DoesNotExist:
            pass
