from django.shortcuts import render


from django.http import JsonResponse
from .models import UserConnection


def handle_friend_request(request):
    connection = UserConnection.objects.filter(id=connection_id, receiver_id=request.user).first()

    if not connection:
        return JsonResponse({'status': 'error', 'message': 'Connection request not found.'}, status=404)
    if action == 'accept':
        if connection.status != UserConnection.Status.PENDING:
            return JsonResponse({'status': 'error', 'message': 'This request has already been processed.'}, status=400)

        connection.status = UserConnection.Status.APPROVED
        connection.save()

        return JsonResponse({'status': 'success', 'message': 'Connection request accepted. You are now connected.'})








