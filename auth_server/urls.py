from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from client_backend import views as client_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/userinfo/', user_views.UserInfoView.as_view(), name='user-info'),
    path('api/logout/', user_views.LogoutView.as_view(), name='logout'),
    path('api/roles/', user_views.RoleListView.as_view(), name='roles'),
    path('api/validate-token/', user_views.ValidateTokenView.as_view(), name='validate-token'),
    path('client/exchange/', client_views.exchange_code, name='client-exchange'),
]
