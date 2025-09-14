from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from oauth2_provider.models import AccessToken, RefreshToken
from django.utils import timezone
from django.contrib.auth import logout
from .serializers import UserSerializer
from .models import User

class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        AccessToken.objects.filter(user=request.user).delete()
        RefreshToken.objects.filter(user=request.user).delete()
        logout(request)
        return Response({'detail':'Logged out and tokens revoked'}, status=status.HTTP_200_OK)

class RoleListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        if getattr(request.user, 'role', None) != 'admin':
            return Response({'detail':'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        users = User.objects.all()
        data = [{'id':u.id,'username':u.username,'role':u.role} for u in users]
        return Response(data)



class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "roles": [g.name for g in user.groups.all()],
        })
class ValidateTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        token_value = request.data.get('token')
        if not token_value:
            return Response({'active': False, 'detail': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            t = AccessToken.objects.get(token=token_value)
            if t.expires < timezone.now():
                return Response({'active': False})
            return Response({'active': True, 'user_id': t.user_id, 'username': t.user.username, 'scope': t.scope, 'expires': t.expires})
        except AccessToken.DoesNotExist:
            return Response({'active': False})
