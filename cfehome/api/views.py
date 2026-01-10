from django.http import JsonResponse,HttpResponse
import json

from tinycss2 import serialize

from products.models import Product
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializer
# Create your views here.


@api_view(['POST'])
def api_home(request,*args,**kwargs):
    """
    DRF api view for home page
    """
    serializer=ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data)
    return Response({'invalid':'not good data'},status=400)