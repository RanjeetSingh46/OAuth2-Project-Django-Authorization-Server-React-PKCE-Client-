from oauth2_provider.oauth2_validators import OAuth2Validator
from django.contrib.auth import get_user_model
from otp_grant.models import OTPCode

User = get_user_model()

class OTPGrantValidator(OAuth2Validator):
    def validate_grant_type(self, request):
        # allow default grant types + our custom 'otp'
        if getattr(request, 'grant_type', None) == 'otp':
            return True
        return super().validate_grant_type(request)

    def validate_user(self, username, password, client, request, *args, **kwargs):
        # For otp grant, 'password' is OTP code
        if getattr(request, 'grant_type', None) == 'otp':
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return False
            # check OTPCode
            otp_qs = OTPCode.objects.filter(user=user, code=password).order_by('-created')
            if not otp_qs.exists():
                return False
            otp = otp_qs.first()
            if otp.is_valid():
                # consume OTP
                otp.delete()
                request.user = user
                return True
            return False
        return super().validate_user(username, password, client, request, *args, **kwargs)
