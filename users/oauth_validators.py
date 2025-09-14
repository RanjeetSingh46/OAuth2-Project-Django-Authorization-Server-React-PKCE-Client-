# users/oauth_validators.py
from oauth2_provider.oauth2_validators import OAuth2Validator
from django.contrib.auth import get_user_model
from otp_grant.models import OTPCode

User = get_user_model()

class OTPGrantValidator(OAuth2Validator):
    """
    Accepts otp grant and also treats password-as-OTP if it looks like OTP.
    Compatible signature for validate_grant_type used by oauthlib/DOT.
    """

    def validate_grant_type(self, client_id, grant_type, client, request, *args, **kwargs):
        # Accept 'otp' at validator-level (though token_proxy maps to password)
        if grant_type == "otp":
            return True
        return super().validate_grant_type(client_id, grant_type, client, request, *args, **kwargs)

    def validate_user(self, username, password, client, request, *args, **kwargs):
        # If grant_type explicitly 'otp' treat as OTP
        if getattr(request, "grant_type", None) == "otp":
            return self._validate_otp_user(username, password, request)

        # Also: if grant_type is 'password' but password looks like OTP (numeric, length 4/6)
        # and there exists an OTPCode for this user with that code, treat it as OTP.
        is_possible_otp = False
        try:
            if getattr(request, "grant_type", None) == "password":
                if isinstance(password, str) and password.isdigit() and len(password) in (4,6):
                    is_possible_otp = True
        except Exception:
            is_possible_otp = False

        if is_possible_otp:
            ok = self._validate_otp_user(username, password, request)
            if ok:
                return True
            # else fallthrough to normal password validation (in case numeric password is real password)

        # fallback to default (password grant normal behavior, PKCE etc.)
        return super().validate_user(username, password, client, request, *args, **kwargs)

    def _validate_otp_user(self, username, otp_code, request):
        # validate OTPCode model, consume if valid
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return False

        otp_qs = OTPCode.objects.filter(user=user, code=otp_code).order_by("-created")
        if not otp_qs.exists():
            return False
        otp = otp_qs.first()
        if otp.is_valid():
            otp.delete()
            # note: oauthlib's request object expects request.user on success
            try:
                request.user = user
            except Exception:
                pass
            return True
        return False
