import random, string
from datetime import timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from otp_grant.models import OTPCode

User = get_user_model()

def generate_numeric_otp(length=6):
    return ''.join(random.choices('0123456789', k=length))

@csrf_exempt
def request_otp(request):
    if request.method != 'POST':
        return JsonResponse({'error':'method_not_allowed'}, status=405)
    username = request.POST.get('username') or request.GET.get('username')
    if not username:
        return JsonResponse({'error':'missing_username'}, status=400)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error':'no_user'}, status=400)
    code = generate_numeric_otp(6)
    expires = timezone.now() + timedelta(minutes=5)
    OTPCode.objects.create(user=user, code=code, expires_at=expires)
    # In dev, print OTP to console; in prod integrate with SMS/email provider.
    print(f"DEBUG OTP for {user.username}: {code}")
    return JsonResponse({'detail':'otp_sent', 'debug_otp': code})  # debug_otp only for dev
