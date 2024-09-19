from rest_framework import serializers
from ride_app_back.users.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username','email', 'cpf', 'picture', 'cnh', 'status', 'balance', 'groups']

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }

    def validate(self, data):
        for field, value in data.items():
            if value is None or value == '':
                raise serializers.ValidationError({field: "This field cannot be empty."})
        return data


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['email'] = self.validated_data.get('email', '')
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
        user.save()
        return user