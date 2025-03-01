from django.shortcuts import get_object_or_404
from rest_framework import status,viewsets,generics
from rest_framework.response import Response
#from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Order
from .serializers import OrderSerializer,OrderIDSerializer
import queue
import threading
import time

from django.db.models import Count,Avg,F,ExpressionWrapper,DurationField

order_queue=queue.Queue()

def process_orders():
    while True:
        order_id=order_queue.get()
        if order_id:
            order=Order.objects.get(order_id=order_id)
            order.status='Processing'
            order.save()
            time.sleep(50)
            order.status='Completed'
            order.save()
            

threading.Thread(target=process_orders,daemon=True).start()

class OrderCreateView(viewsets.ViewSet):
    def post(self,request):
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            order=serializer.save()
            order_queue.put(order.order_id)
            return Response({'order_id': order.order_id, 'status': order.status}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        try:
            order=Order.objects.get(order_id=pk)
            return Response({'order_id':order.order_id,'status':order.status})
        except Order.DoesNotExist:
            return Response({'error':'Order not found'},status=status.HTTP_404_NOT_FOUND)

class OrderIDView(generics.ListAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderIDSerializer


def Metrics(request):
    total_orders=Order.objects.count()
    #completed_orders = Order.objects.filter(status="Completed")

    res = Order.objects.filter(status="Completed").aggregate(
        avg_time=Avg(
            ExpressionWrapper(F("updated_at") - F("created_at"), output_field=DurationField()))
    )
    ["avg_time"] or 0
    avg_process_time=res.get("avg_time",0).total_seconds() if res["avg_time"] else 0 
    status_counts=Order.objects.values('status').annotate(count=Count('status'))
    return JsonResponse({
        'total_orders':total_orders,
        'avg_process_time':avg_process_time,
        'status_counts':{s['status']: s['count'] for s in status_counts}
    })


