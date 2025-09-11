# OAuth2 Project (Django Authorization Server + React PKCE Client)

This repository contains a working example implementing OAuth2 Authorization Code + PKCE using Django OAuth Toolkit, a React PKCE client, and optional Docker setup.

## What's included
- Django OAuth Toolkit (authorization server)
- Authorization Code (PKCE) + Refresh Token flow
- Token rotation + configurable expiry
- Custom User model with role field
- APIs: token issuance (DOT), token introspection, validate-token, userinfo, logout (revokes tokens), roles
- React PKCE client (login, callback, token exchange, profile)
- Docker & docker-compose for Postgres + web

## Local (no Docker) quick setup
1. Create virtualenv and install dependencies:
 ```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```
2. Setup database (sqlite default will work, or use Postgres):
   - By default settings use sqlite for quick local dev.
   - For Postgres, create DB and set DB_* env vars.
   ```env
   DB_HOST=db
   # OAuth Client (generated via create_oauth_app)
   OAUTH_CLIENT_ID=

   # React App URLs
   OAUTH_REDIRECT_URI=http://localhost:3000/callback
   OAUTH_AUTH_URL=http://localhost:8000/o/authorize/
   OAUTH_TOKEN_URL=http://localhost:8000/o/token/
   API_USERINFO_URL=http://localhost:8000/api/userinfo/

   # SECURITY
   SECRET_KEY=
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # DATABASE (local Postgres example)
   DB_NAME=oauth_db
   DB_USER=
   DB_PASSWORD=
   DB_HOST=localhost
   DB_PORT=5432

   # OAUTH2 SETTINGS
   ACCESS_TOKEN_EXPIRE_SECONDS=3600         # 1 hour
   REFRESH_TOKEN_EXPIRE_SECONDS=1209600     # 14 days
   ROTATE_REFRESH_TOKEN=True

   # DJANGO SUPERUSER (optional auto-create)
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=admin123

   # CORS (for React dev)
   CORS_ALLOWED_ORIGINS=http://localhost:3000

   ```
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create superuser and seed demo users:
   ```bash
   python manage.py createsuperuser
   python manage.py seed_demo_users
   ```
5. Create OAuth app (PKCE public client):
   ```bash
   python manage.py create_oauth_app
   ```
   Note the printed Client ID and put it into react-client/src/config.js
6. Run server:
   ```bash
   python manage.py runserver
   ```
7. React client:
   ```bash
   cd react-client
   npm install
   # open react-client/src/config.js and set OAUTH_CLIENT_ID
   npm start
   ```
8. Test: open http://localhost:3000 -> Login -> Authorize -> Fetch Profile

## Docker setup
1. Copy .env.example to .env and adjust values (for docker DB_HOST should be 'db')
2. Start:
   ```bash
   docker-compose up --build -d
   ```
3. Run migrations and create oauth app:
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   docker-compose exec web python manage.py seed_demo_users
   docker-compose exec web python manage.py create_oauth_app
   ```

## Notes
- For SPAs use PKCE. For confidential clients use server-side secret and `/client/exchange/` endpoint.
- In production set DEBUG=False, use HTTPS, set SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE.

--

## Screenshot
![Screenshot](./page1.png)
![Screenshot](./page2.png)
![Screenshot](./page3.png)
![Screenshot](./page4.png)
![Screenshot](./page5.png)
![Screenshot](./page6.png)
![Screenshot](./page7.png)
![Screenshot](./page8.png)
