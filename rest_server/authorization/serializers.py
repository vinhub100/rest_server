from rest_framework.serializers import ModelSerializer, EmailField, ValidationError, CharField, ChoiceField
from django.contrib.auth.models import User
from .models import UserProfile


Roles = ["Player", "Author"]


class SignUpSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')
    role = ChoiceField(choices=Roles)

    class Meta:
        model = User
        fields = ['username', 'email', 'email2', 'password', 'role']
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        data = self.get_initial()
        email2 = data.get('email2')
        email1 = value
        if email1 != email2:
            raise ValidationError('Both Emails must be same')
        usr = User.objects.filter(email = email1)
        if usr.exists():
            raise ValidationError('This email already exists')
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        if email1 != value:
            raise ValidationError('Both Emails must be same')
        return value

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        usr = User(username=username, email=email)
        usr.set_password(password)
        usr.save(force_insert=True)
        user_prof = UserProfile(user=usr, role=validated_data.get('role'))
        user_prof.save()
        return validated_data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class UserRoleSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role']

