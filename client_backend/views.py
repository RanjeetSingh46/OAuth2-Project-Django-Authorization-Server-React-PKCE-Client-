import os, requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

TOKEN_URL = os.environ.get('OAUTH_TOKEN_URL', 'http://localhost:8000/o/token/')
CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET', '')
REDIRECT_URI = os.environ.get('OAUTH_REDIRECT_URI', 'http://localhost:3000/callback')

@csrf_exempt
def exchange_code(request):
    if request.method != 'POST':
        return JsonResponse({'detail':'Method not allowed'}, status=405)
    code = request.POST.get('code')
    verifier = request.POST.get('code_verifier')
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
    }
    if CLIENT_SECRET:
        payload['client_secret'] = CLIENT_SECRET
    if verifier:
        payload['code_verifier'] = verifier
    r = requests.post(TOKEN_URL, data=payload)
    print("request", r.status_code, r.json())
    return JsonResponse(r.json(), status=r.status_code)
