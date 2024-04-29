from rest_framework import serializers
from ride_app_back.users.models import User, Pilot


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ['id','name','surname','email','cpf','birthday','balance','number','picture']

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }

class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilot
        fields = ['user','motorcycle','cnh','status']