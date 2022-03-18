from datetime import datetime
from django.contrib.auth.models import User
from keyapi.models import KeyUser
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class KeyUserView(ViewSet):
    def list(self, request):
        users = KeyUser.objects.all()
        serializer = KeyUserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            keyUser = KeyUser.objects.get(pk=pk)
            serializer = KeyUserSerializer(keyUser)
            return Response(serializer.data)
        except KeyUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False)
    def current(self, request):
        """Only get actors back that are currently active on a book"""

        key_user = KeyUser.objects.get(user=request.auth.user)
        serializer = KeyUserSerializer(key_user)
        return Response(serializer.data)
    
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user types
    """
    class Meta:
        model = User
        depth = 1
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'date_joined']


class KeyUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = KeyUser
        fields = ['id', 'user', 'institution', 'field']