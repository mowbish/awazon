from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'is_suspended',
            'gender',
            'auth_level',
            'phone_number',
            'birthday'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'email': {'required': True},
            'phone_number': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            is_suspended=validated_data.get('is_suspended', False),
            gender=validated_data.get('gender'),
            auth_level=validated_data.get('auth_level', 0),
            phone_number=validated_data['phone_number'],
            birthday=validated_data.get('birthday'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'birthday', 'gender')
        read_only_fields = ('username',)

    def update(self, instance, validated_data):
        [setattr(instance, field, validated_data.get(field, getattr(instance, field))) for field in validated_data]
        instance.save()
        return instance