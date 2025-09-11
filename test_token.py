#!/usr/bin/env python3
"""
Test script to debug OAuth2 token endpoint
"""
import os
import requests
import urllib.parse

# Load environment variables
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_server.settings')
django.setup()

from oauth2_provider.models import Grant

# Test token request with a sample authorization code
def test_token_request():
    token_url = 'http://localhost:8000/o/token/'
    client_id = 'JqZGacrvNVSOgULedbz4vF2ZqmswRVRqk15XZc5u'
    redirect_uri = 'http://localhost:3000/callback'
    
    print("=== OAuth2 Token Request Test ===")
    print(f"Token URL: {token_url}")
    print(f"Client ID: {client_id}")
    print(f"Redirect URI: {redirect_uri}")
    
    # Check if we have any authorization grants
    grants = Grant.objects.filter(application__client_id=client_id)
    print(f"Existing grants: {grants.count()}")
    
    if grants.exists():
        latest_grant = grants.last()
        print(f"Latest grant code: {latest_grant.code}")
        print(f"Latest grant expires: {latest_grant.expires}")
        
        # Test the token request
        payload = {
            'grant_type': 'authorization_code',
            'code': latest_grant.code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'code_verifier': 'test_verifier',  # This should match the challenge
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        print(f"Request payload: {payload}")
        
        try:
            response = requests.post(token_url, data=payload, headers=headers)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response body: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    else:
        print("No authorization grants found. You need to authorize first.")

if __name__ == '__main__':
    test_token_request()
