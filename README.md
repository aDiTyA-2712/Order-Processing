# Order Processing System

## 📖 Overview
The **Order Processing System** is a backend service designed to handle order creation, status tracking, and order metrics using Django and Django REST Framework (DRF). It includes an **in-memory queue** for asynchronous order processing and supports **high concurrency** with load testing using Locust.

## 🚀 Features
- **Order Management:** Create orders and check their status.
- **Asynchronous Processing:** Uses an in-memory queue to handle orders in the background.
- **Metrics API:** Provides analytics like total orders, average processing time, and order status counts.
- **Scalability Testing:** Simulate **1,000+ concurrent requests** using Locust.

---

## 🏗️ Project Structure

	ecommerce/                  # Main Django project
	│
	├── __pycache__/            # Python bytecode cache
	├── __init__.py             # Initialization file
	├── asgi.py                 # ASGI entry point for async deployment
	├── celery.py               # Celery configuration for async tasks
	├── settings.py             # Django settings (e.g., database, installed apps)
	├── urls.py                 # Project-wide URL routing
	├── wsgi.py                 # WSGI entry point for deployment
	│
	├── orders/                 # Django app for order management
	│   ├── __pycache__/        # Python bytecode cache
	│   ├── migrations/         # Database migrations
	│   ├── __init__.py         # Initialization file
	│   ├── admin.py            # Admin panel configuration
	│   ├── apps.py             # App configuration
	│   ├── models.py           # Order model (database schema)
	│   ├── serializers.py      # DRF serializers for API data formatting
	│   ├── tasks.py            # Celery tasks for background processing
	│   ├── tests.py            # Unit and integration tests
	│   ├── urls.py             # App-specific URL routing
	│   └── views.py            # API views (order processing, metrics)
	│
	├── locustfile.py           # Load testing script using Locust
	├── manage.py               # Django command-line utility
	└── README.md               # Documentation (you are here!)

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

- git clone https://github.com/aDiTyA-2712/Order-Processing.git
- cd Order-Processing/ecommerce>

### 2️⃣ Create a Virtual Environment & Activate it(If using)
- python -m venv venv
- source venv/bin/activate  # On macOS/Linux
- venv\Scripts\activate     # On Windows

### 3️⃣ Install Dependencies
- pip install -r requirements.txt

### 4️⃣ Apply Migrations & Start Server
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

📌 API Endpoints

1️⃣ Create an Order

	~ Endpoint: curl -X POST http://127.0.0.1:8000/api/orders/create/ -H "Content-Type: application/json" -d '
	
	~ Request Body:
	
		{
			"user_id": 645,
			"order_id": "userTest23",
			"item_ids": [890, 563],
			"total_amount": 1650.78,
			"status": "Processing"
		}
		
	~ Response:

		{
			"order_id": "ORD564-567",
			"status": "Processing"
		}
		
2️⃣ Get Order Status

	~ Endpoint: curl -X GET http://127.0.0.1:8000/api/orders/<order_id>/status/
				eg http://127.0.0.1:8000/api/orders/ORD564-567/status/
				
	~ Response:

		{
			"order_id": "ORD564-567",
			"status": "Completed"
		}
		
3️⃣ Get All Order IDs

	~ Endpoint: curl -X GET http://127.0.0.1:8000/api/orders/ids/
	
	~ Response:

		[
			{
				"order_id": "ORD747-815"
			},
			{
				"order_id": "ORD853-000"
			},
			{
				"order_id": "ORD976-52"
			},
			{
				"order_id": "ORD024-697"
			},
		]
		
4️⃣ Get Order Metrics

	~ Endpoint: GET api/metrics/
	
	~ Response:

		{
			"total_orders": 100,
			"avg_process_time": 30.5,
			"status_counts": {
				"Pending": 10,
				"Processing": 5,
				"Completed": 85
			}
		}
⚡ Asynchronous Order Processing

	The system uses an in-memory queue (queue.Queue) to process orders in the background.

	How It Works:
	
		When a new order is placed, it's added to the order queue.
		A background thread fetches the order from the queue.
		The order status is updated to "Processing", then after 50 seconds, it's marked "Completed".
	
	Implementation for this you can see in views.py in method 'process_orders'(https://github.com/aDiTyA-2712/Order-Processing/blob/main/orders/views.py)
	
📈 Load Testing with Locust

	We use Locust to simulate high traffic and test the system under 1,000 concurrent users.
	
	steps:
		1.pip install locust
		2.Run the load test in terminal: locust -f locustfile.py
		
			example of locustfile.py:
			
			from locust import HttpUser, task, between

			class OrderLoadTest(HttpUser):
				wait_time = between(1, 3)
			
				@task(1)
				def create_order(self):
					self.client.post("/orders/", json={"product_name": "Phone", "quantity": 2})
			
				@task(2)
				def get_orders(self):
					self.client.get("/orders/ids/")

		3.Then, open http://localhost:8089 in a browser and start the test.
		4.Enter Number of Users (e.g., 1000)
		5.Set Spawn Rate (e.g., 10 users per second)
		6.Set Host: http://127.0.0.1:8000/ (your Django server)
		7.Click Start
		
🛠️ Scalability Considerations

	🔹 Handling 1,000+ Concurrent Orders
	
		- Use Celery + Redis instead of an in-memory queue.
		- Deploy with Gunicorn & Nginx for better concurrency.
		- Use PostgreSQL/MySQL for scalable DB operations.
		- Enable Caching (Redis/Memcached) to reduce DB hits.
		
	🤝 Contributing
	
		Pull requests are welcome! For major changes, please open an issue first to discuss the proposed changes.

			- Fork the repo.
			- Create a new branch (git checkout -b feature-branch).
			- Commit your changes (git commit -m "Added new feature").
			- Push to your branch (git push origin feature-branch).
			- Open a PR.

✨ Author

- Aditya Kumar
	
- GitHub: @aDiTyA-2712 (https://github.com/aDiTyA-2712/)