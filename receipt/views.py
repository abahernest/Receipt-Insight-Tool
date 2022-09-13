from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView

# serializers
from .serializer import DelimeterSerializer, DocumentSerializer, BlockSerializer
# models
from .models import Delimeter, Document, Block


class ReceiptView (APIView):

    def get (self,request):
        try:
            return JsonResponse({
                "code":200,
                "data": "peace",
                "message": "success"
            })

        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "code": 500,
                    'message': "Internal Server Error",
                    "error": e.args
                },
                status=500)