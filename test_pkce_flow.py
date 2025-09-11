#!/usr/bin/env python3
"""
Test the complete PKCE flow with the Django OAuth2 server
"""
import os
import requests
import urllib.parse
from base64 import urlsafe_b64encode
import hashlib
import secrets
import string

# Django setup
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_server.settings')
django.setup()

from oauth2_provider.models import Grant, Application

def generate_pkce_pair():
    """Generate PKCE verifier and challenge"""
    # Generate code verifier (43-128 characters from allowed set)
    code_verifier = ''.join(secrets.choice(
        string.ascii_letters + string.digits + '-._~'
    ) for _ in range(64))
    
    # Generate code challenge using SHA256
    challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = urlsafe_b64encode(challenge).decode('utf-8').rstrip('=')
    
    return code_verifier, code_challenge

def test_pkce_flow():
    """Test the complete PKCE flow"""
    print("=== Testing Complete PKCE Flow ===")
    
    # Configuration
    client_id = 'JqZGacrvNVSOgULedbz4vF2ZqmswRVRqk15XZc5u'
    redirect_uri = 'http://localhost:3000/callback'
    auth_url = 'http://localhost:8000/o/authorize/'
    token_url = 'http://localhost:8000/o/token/'
    
    # Generate PKCE pair
    code_verifier, code_challenge = generate_pkce_pair()
    print(f"Generated verifier: {code_verifier}")
    print(f"Generated challenge: {code_challenge}")
    
    # Step 1: Simulate authorization request
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'read',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    
    auth_url_full = f"{auth_url}?{urllib.parse.urlencode(auth_params)}"
    print(f"\\nAuthorization URL: {auth_url_full}")
    print("Please visit this URL in a browser, authorize, and copy the 'code' parameter from the redirect URL.")
    
    # For testing, let's try to find the most recent grant
    try:
        app = Application.objects.get(client_id=client_id)
        recent_grants = Grant.objects.filter(application=app).order_by('-created')
        
        if recent_grants.exists():
            latest_grant = recent_grants.first()
            print(f"\\nFound recent grant: {latest_grant.code}")
            print(f"Grant expires: {latest_grant.expires}")
            print(f"Grant challenge: {latest_grant.code_challenge}")
            print(f"Grant challenge method: {latest_grant.code_challenge_method}")
            
            # Test token exchange with the actual challenge from the grant
            print(f"\\nTesting token exchange...")
            
            # We need to get the original verifier that was used for this grant
            # This is a limitation - we can't easily test with old grants
            print("Note: Cannot test token exchange with old grants as we don't have the original verifier.")
            print("Please use the authorization URL above to generate a fresh code with the known verifier.")
            
    except Exception as e:
        print(f"Error checking grants: {e}")
    
    print(f"\\nFor manual testing, use these values:")
    print(f"Verifier: {code_verifier}")
    print(f"Challenge: {code_challenge}")

if __name__ == '__main__':
    test_pkce_flow()
