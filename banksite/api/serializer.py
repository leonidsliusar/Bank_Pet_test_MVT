from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, User


class WalletSerializer(serializers.Serializer):
    wallet_id = serializers.CharField()
    balance = serializers.DecimalField(max_digits=20, decimal_places=2)


class TransactionDataSerializer(serializers.Serializer):
    source = serializers.CharField()
    recipient = serializers.CharField()
    quantity = serializers.CharField()


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name']
