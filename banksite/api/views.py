from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsWalletOwner
from api.serializer import WalletSerializer, TransactionDataSerializer
from bank.models import Wallet
from bank.services import create_wallet, make_transaction


class ListWalletView(APIView):
    permission_classes = [IsWalletOwner]

    def get(self, request, user_id: int):  # get all wallets
        query = Wallet.objects.filter(user_id=user_id).select_related('user').only(
            'balance', 'wallet_id', 'user__first_name')
        response = Response({'error': f'User with id {user_id} haven\'t wallets'}, status=404)
        if query:
            wallets_data = WalletSerializer(query, many=True).data
            user_first_name = query[0].user.first_name
            response = Response({user_first_name: wallets_data})
        return response

    def post(self, request, user_id: int):  # generate new wallet
        create_wallet(user_id)
        response = Response(status=201)
        return response


class DetailWalletView(APIView):
    permission_classes = [IsWalletOwner]

    def get(self, request, user_id: int, wallet_id: str):  # get specific one wallet
        query = Wallet.objects.filter(pk=wallet_id, user_id=user_id).select_related('user').only(
        'balance', 'wallet_id', 'user__first_name')
        response = Response({'error': f'wallet {wallet_id} doesn\'t exists'}, status=404)
        if query:
            wallets_data = WalletSerializer(query, many=True).data
            user_first_name = query[0].user.first_name
            response = Response({user_first_name: wallets_data})
        return response

    def delete(self, request, user_id: int, wallet_id: str):  # delete specific one wallet
        try:
            wallet = Wallet.objects.get(pk=wallet_id, user_id=user_id)
            if wallet.balance != 0:
                response = Response({'error': 'the wallet isn\'t empty'}, status=400)
            else:
                wallet.delete()
                response = Response(status=200)
        except ObjectDoesNotExist:
            response = Response({'error': f'wallet {wallet_id} doesn\'t exists'}, status=404)
        return response


class TransactionView(APIView):
    permission_classes = [IsWalletOwner]

    def post(self, request, user_id: int):  # make transaction
        serializer = TransactionDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = make_transaction(request, **serializer.data)
        match message:
            case 'Transaction successful':
                code = 200
            case _:
                code = 400
        response = Response({message}, status=code)
        return response
