from django.urls import path
from .views import OrderCreateView,Metrics,OrderIDView

urlpatterns=[
    path('orders/',OrderCreateView.as_view({'post':'post'}),name='create-order'),
    path('orders/<str:pk>/status/',OrderCreateView.as_view({'get':'retrieve'}),name='order_status'),
    path('metrics/',Metrics,name='metrics'),
    path('orders/ids/',OrderIDView.as_view(),name='order-list'), # To get all the order_id and get to the status of any particular order_id
]
