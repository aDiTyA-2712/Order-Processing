from rest_framework import serializers
from .models import Order
import random,string
from .tasks import process_order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['user_id','order_id','item_ids','total_amount','status','created_at','updated_at']

    def create(self,validated_data):
        order = super().create(validated_data)
        process_order.delay(order.order_id)  # for queuing the order for processing
        return order

class OrderIDSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['order_id']        