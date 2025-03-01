''''
This implementation is used for the mentioned scalability of the django service that 
the system can handle 1,000 concurrent orders (simulate load).
And for this I have used Locust which is a Python load testing tool
which randomly generates n requests(here 1000) in t seconds(here 10)
'''

from locust import HttpUser, task, between
import random
import string
import json

class OrderLoadTest(HttpUser):
    wait_time = between(1, 3)  # Wait time between requests (1-3 seconds)

    @task
    def create_order(self):
        
        order_id = "ORD" + "".join(random.choices(string.digits, k=4)) + "-"+"".join(random.choices(string.digits, k=3))
        status=["Processing","Pending","Completed"]
        payload = {
            "user_id": random.randint(100, 999),
            "order_id": order_id,
            "item_ids": [random.randint(500, 1000), random.randint(500, 1000)],
            "total_amount": round(random.uniform(100, 5000), 2),
            "status": random.choice(status)
        }

        headers = {"Content-Type": "application/json"}
        self.client.post("api/orders/", data=json.dumps(payload), headers=headers)

    @task
    def get_orders(self):
        """Simulate fetching all order IDs"""
        self.client.get("api/orders/ids/")

