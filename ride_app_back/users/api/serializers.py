from rest_framework import serializers
from ride_app_back.users.models import User


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
