from django.shortcuts import render
from rest_framework import generics,mixins,authentication,permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .permissions import IsStaffEditorPermission
from api.authentication import TokenAuthentication
# Create your views here.
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication,TokenAuthentication]
    permission_classes = [IsStaffEditorPermission]

product_list_api_view = ProductListCreateAPIView.as_view()

class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
product_destroy_api_view = ProductDestroyAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance= serializer.save()
        if not instance.content:
            instance.content=instance.title
product_Update_api_view = ProductUpdateAPIView.as_view()

@api_view(['GET', 'POST'])
def product_alt_view(request, *args, **kwargs):
    method=request.method
    pk=kwargs.get('pk')
    if method == 'GET':
        if pk is not None:
            output=get_object_or_404(Product,pk=pk)
        else:
            output = Product.objects.all()

        serializer = ProductSerializer(output, many= False if pk else True )
        return Response(serializer.data)

    elif method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title=serializer.validated_data['title']
            content=serializer.validated_data['content']
            if not content:
                content=title
            serializer.save(content=content)
            return Response(serializer.data)

    return Response({'detail': 'Method Not Allowed'})


class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    def get(self,request,*args,**kwargs):
        print(args,kwargs)
        pk=kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request,*args,**kwargs)
        return self.list(request,*args,**kwargs)


    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

product_mixin_view = ProductMixinView.as_view()





