from django.contrib import admin
from users.token_proxy import token_proxy
from django.urls import path, include
from users import views as user_views
from users import token_endpoints
from users.otp_views import request_otp

from client_backend import views as client_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/token/', token_proxy, name='oauth2_token'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/userinfo/', user_views.UserInfoView.as_view(), name='user-info'),
    path('api/profile/', user_views.ProfileView.as_view(), name='profile'),
    path('api/logout/', user_views.LogoutView.as_view(), name='logout'),
    path('api/roles/', user_views.RoleListView.as_view(), name='roles'),
    path('api/validate-token/', user_views.ValidateTokenView.as_view(), name='validate-token'),
    path('client/exchange/', client_views.exchange_code, name='client-exchange'),
    path('api/token/password/', token_endpoints.token_by_password, name='token-by-password'),
    path('api/token/otp/', token_endpoints.token_by_otp, name='token-by-otp'),
    path('api/request-otp/', request_otp, name='request-otp'),
]
