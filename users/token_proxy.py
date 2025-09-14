# users/token_proxy.py
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.views import TokenView
from django.utils.decorators import method_decorator

@csrf_exempt
def token_proxy(request, *args, **kwargs):
    """
    If incoming POST has grant_type=otp, rewrite it into a password grant
    where password=<otp>. Keep the 'otp' field as well.
    Then delegate to DOT's TokenView.
    """
    if request.method == "POST":
        try:
            # request.POST is a QueryDict (immutable) — make a mutable copy
            pd = request.POST.copy()
            if pd.get("grant_type") == "otp":
                otp_val = pd.get("otp") or pd.get("password")
                if otp_val:
                    # put OTP into password so oauthlib handles it via password grant
                    pd["password"] = otp_val
                    pd["grant_type"] = "password"
                    # assign back to request so TokenView sees modified data
                    request._post = pd
                    request._files = request.FILES
        except Exception:
            # if anything goes wrong, we still fall back to TokenView
            pass

    # Delegate to DOT TokenView (this will handle password, client_credentials, auth_code etc.)
    view = TokenView.as_view()
    return view(request, *args, **kwargs)
