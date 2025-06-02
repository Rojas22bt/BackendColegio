from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@csrf_exempt
def simple_post(request):
    if request.method == 'POST':
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    return Response({'status': 'error', 'message': 'Only POST allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)