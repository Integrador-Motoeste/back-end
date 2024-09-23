from rest_framework import serializers
from ride_app_back.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.serializers import JWTSerializer
from ride_app_back.motorcycles.api.serializers import MotorcycleSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        picture = serializers.ImageField()

        model = User
        fields = ['id', 'first_name', 'last_name', 'username','email', 'cpf', 'picture', 'cnh', 'status', 'balance', 'groups']

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class UserCreateSerializer(JWTSerializer, UserSerializer):

    pass


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)
    picture = serializers.ImageField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['email'] = self.validated_data.get('email', '')
        data['cpf'] = self.validated_data.get('cpf', '')
        return data

    def validate_email(self, email):
        return email

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.cpf = self.cleaned_data.get('cpf')
        user.picture = self.validated_data.get('picture')
        user.save()
        return user


class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'cpf', 'cnh']


class TurnUserPilotSerializer(serializers.Serializer):
    pilot = PilotSerializer()
    motorcycle = MotorcycleSerializer()
