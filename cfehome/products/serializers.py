from rest_framework import serializers
from .models import Product
from rest_framework.reverse import reverse
import datetime
class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url= serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk')
    #clock=serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(write_only=True)
    class Meta:
        model = Product
        fields = [
                'url',
                'edit_url',
                  'pk',
                'email',
                  'title',
                  'content',
                  'price',
                  #'clock',
                  'sale_price',
                  'my_discount'
                  ]

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    #def get_clock(self,obj):
     #   return datetime.datetime.now().strftime('%H:%M:%S')
    def get_edit_url(self, obj):
        # return f"/api/products/{obj.pk}/"
        request=self.context.get('request')
        if request is None:
            return None
        return reverse("product-detail",kwargs={'pk':obj.pk},request=request)
    def get_my_discount(self,obj):
        if not hasattr(obj,'id') and not isinstance(obj,Product):
            return None
        return obj.get_discount()