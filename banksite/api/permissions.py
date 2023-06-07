from rest_framework.permissions import BasePermission


class IsWalletOwner(BasePermission):
    def has_permission(self, request, view):
        query_string = view.kwargs['user_id']
        token = request.auth
        token_user_id = token.payload.get("user_id")
        return bool(request.user and request.user.is_authenticated and query_string == token_user_id)
