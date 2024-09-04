from rest_framework import serializers
from ride_app_back.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ['id','username','surname','email','cpf','birthday','phone','picture']

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }
