from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from apps.users.api.v1.serializers import UserSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        'create': (AllowAny,),
        'retrieve': (IsAdminUser,),
        'list': (IsAdminUser,),
        'update': (IsAdminUser,),
        'destroy': (IsAdminUser,),
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data = {'user_id': str(user.id), 'username': user.username}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update_me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = UserProfileSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'put'], name='Get/Update My Profile')
    def profile(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.me(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update_me(request, *args, **kwargs)