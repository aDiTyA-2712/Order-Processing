from django.db import models

import random,string

def generate_order_id():
    return "ORD" + "".join(random.choices(string.digits, k=4))+"-"+"".join(random.choices(string.digits, k=3))

class Order(models.Model):
    STATUS_CHOICES=[
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Completed','Completed'),
    ]
    user_id=models.CharField(max_length=100)
    #ord_id=models.CharField(max_length=50)
    order_id=models.CharField(default=generate_order_id,max_length=100,unique=True,editable=False,primary_key=True)
   
    item_ids=models.JSONField()
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"Order {self.order_id} ({self.status})"
