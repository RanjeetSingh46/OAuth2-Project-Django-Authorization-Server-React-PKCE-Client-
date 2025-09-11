import requests
import json

# Test the token endpoint
url = 'http://localhost:8000/o/token/'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Python-Test/1.0'
}

# Test data (use a recent code from the logs)
data = {
    'grant_type': 'authorization_code',
    'code': '0afBJ8camejuG3hUttHjmhhhiEMYfx',  # Use the latest code from server logs
    'redirect_uri': 'http://localhost:3000/callback',
    'client_id': 'JqZGacrvNVSOgULedbz4vF2ZqmswRVRqk15XZc5u',
    'code_verifier': 'test_verifier_that_should_match_challenge'
}

print("Making token request...")
print(f"URL: {url}")
print(f"Headers: {headers}")
print(f"Data: {data}")

try:
    response = requests.post(url, data=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response text: {response.text}")
    
    if response.headers.get('content-type', '').startswith('application/json'):
        try:
            json_response = response.json()
            print(f"JSON Response: {json.dumps(json_response, indent=2)}")
        except:
            print("Could not parse JSON response")
            
except Exception as e:
    print(f"Error: {e}")
