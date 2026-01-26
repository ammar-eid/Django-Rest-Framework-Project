from django.shortcuts import render
from rest_framework import generics,mixins,authentication,permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.mixins import StaffEditorPermissionMixin
from api.authentication import TokenAuthentication
# Create your views here.
from .models import Product
from .serializers import ProductSerializer
from .viewsets import ProductGenericViewSet

class ProductListCreateAPIView(StaffEditorPermissionMixin
    ,generics.ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication,TokenAuthentication]


product_list_create_api_view = ProductListCreateAPIView.as_view()

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

class ProductDetailAPIView(
StaffEditorPermissionMixin
,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

product_detail_view = ProductDetailAPIView.as_view()


@api_view(['GET', 'POST'])
def product_detail_view(request, *args, **kwargs):
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
    ProductGenericViewSet
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

product_mixin_view = ProductMixinView.as_view({'get':'list'})





