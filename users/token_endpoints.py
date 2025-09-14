# users/token_endpoints.py
import uuid
from datetime import timedelta
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from django.utils import timezone
from otp_grant.models import OTPCode 

SERVICE_KEY_HEADER = "HTTP_X_SERVICE_KEY"  # header name: X-Service-Key

@csrf_exempt
def token_by_password(request):
    """
    Secure server-side token issuance using username/password.
    Caller must provide header: X-Service-Key: <SERVICE_API_KEY>
    """
    if request.META.get(SERVICE_KEY_HEADER) != getattr(settings, "SERVICE_API_KEY", None):
        return JsonResponse({"error": "unauthorized"}, status=401)
    if request.method != "POST":
        return JsonResponse({"error": "method_not_allowed"}, status=405)

    username = request.POST.get("username")
    password = request.POST.get("password")
    if not username or not password:
        return JsonResponse({"error": "missing_credentials"}, status=400)

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"error": "invalid_credentials"}, status=400)

    # Use a confidential Application (service app) to associate tokens with
    app = Application.objects.filter(client_type=Application.CLIENT_CONFIDENTIAL).first()
    if not app:
        return JsonResponse({"error": "no_service_app"}, status=500)

    expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token_str = uuid.uuid4().hex
    access_token = AccessToken.objects.create(
        user=user, scope="read", expires=expires, token=access_token_str, application=app
    )
    refresh_token = RefreshToken.objects.create(user=user, token=uuid.uuid4().hex, application=app, access_token=access_token)

    return JsonResponse({
        "access_token": access_token.token,
        "refresh_token": refresh_token.token,
        "token_type": "Bearer",
        "expires_in": oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        "scope": access_token.scope,
    })



@csrf_exempt
def token_by_otp(request):
    if request.headers.get("X-Service-Key") != getattr(settings, "SERVICE_API_KEY", None):
        return JsonResponse({"error": "unauthorized"}, status=401)
    if request.method != "POST":
        return JsonResponse({"error": "method_not_allowed"}, status=405)

    username = request.POST.get("username")
    otp = request.POST.get("otp")
    if not username or not otp:
        return JsonResponse({"error": "missing_parameters"}, status=400)

    User = get_user_model()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "no_user"}, status=400)

    # ✅ Check OTP from DB
    otp_qs = OTPCode.objects.filter(user=user, code=otp).order_by("-created")
    if not otp_qs.exists():
        return JsonResponse({"error": "invalid_otp"}, status=400)

    otp_obj = otp_qs.first()
    if not otp_obj.is_valid():
        return JsonResponse({"error": "expired_otp"}, status=400)

    # consume OTP so it can't be reused
    otp_obj.delete()

    # ✅ Create token (same as before)
    app = Application.objects.filter(client_type=Application.CLIENT_CONFIDENTIAL).first()
    if not app:
        return JsonResponse({"error": "no_service_app"}, status=500)

    expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token_str = uuid.uuid4().hex
    access_token = AccessToken.objects.create(
        user=user, scope="read", expires=expires, token=access_token_str, application=app
    )
    refresh_token = RefreshToken.objects.create(
        user=user, token=uuid.uuid4().hex, application=app, access_token=access_token
    )

    return JsonResponse({
        "access_token": access_token.token,
        "refresh_token": refresh_token.token,
        "token_type": "Bearer",
        "expires_in": oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        "scope": access_token.scope,
    })
