from rest_framework.serializers import ModelSerializer, Serializer, CharField
from account.models import User


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password")

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class SingInSerializer(Serializer):
    username = CharField(min_length=2, max_length=255, required=True)
    password = CharField(min_length=5, max_length=20, required=True)
