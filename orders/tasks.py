from celery import shared_task
from .models import Order

@shared_task
def process_order(order_id):
    #Here we are simulating the order processing
    try:
        order = Order.objects.get(order_id=order_id)
        order.status = "Processing"
        order.save()
        print(f"Processed Order: {order_id}")
    except Order.DoesNotExist:
        print(f"Order {order_id} not found")
