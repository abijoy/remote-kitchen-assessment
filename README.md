# API Backend (remote-kitchen)

## How to run the project

### Clone the repository

`https://github.com/abijoy/remote-kitchen-assessment.git`

`cd remote-kitchen-assessment`

### Install the required packages

First create and activate virtual environment then install the required packages.

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install -r requirements.txt`

### Set up the .env file

`cat .env.example > .env`

In your `.env` set the following environment variables:

STRIPE CONFIG FOR PAYMENT

- `STRIPE_SECRET_KEY`: Your Stripe Testing Secret key
- `WEBHOOK_ENDPOINT_SECRET_KEY`: Webhook endpoint where stripe will send notifications about payment.

### Now perform database migration

`python manage.py migrate`

## Run the server

`python manage.py runserver`

the application will be running on **http://127.0.0.1:8000/**

### Sample Users credentials to interact with the system

### Create superuser to access admin panel

`python manage.py createsuperuser`

## Restaurant API

### List All The Restaurants or Create a new Restaurant

Endpoint: `POST /api/v1/restaurants/` : Create a new restaurant

Endpoint: `GET /api/v1/restaurants/` : Get all the Restaurants by the requested user as an owner/employee

### Retrieve/Update/Delete a Restaruant

Endpoint: `GET /api/v1/restaurants/{pk}/`: Get the restaurant details

Endpoint: `PUT /api/v1/restaurants/{pk}/`: Update the restaurant details

Endpoint: `PATCH /api/v1/restaurants/{pk}/`: Partial update the restaurant details

Endpoint: `DELETE /api/v1/restaurants/{pk}/`: Delete the restaurant

### Create a new Menu for specific restaurant

Endpoint: `POST /api/v1/restaurants/{pk}/menus/`: Create a new menu

Endpoint: `GET /api/v1/restaurants/{pk}/menus/`: List all the menu

### Retrieve/Update/Delete a Menu

Endpoint: `GET /api/v1/restaurants/{pk}/menus/{menu_id}`: Get the menu details

Endpoint: `PUT /api/v1/restaurants/{pk}/menus/{menu_id}`: Update the menu details

Endpoint: `PATCH /api/v1/restaurants/{pk}/menus/{menu_id}`: Partial update the menu details

Endpoint: `DELETE /api/v1/restaurants/{pk}/menus/{menu_id}`: Delete the menu

### Create a new Item under for specific restaurant's specific menu

Endpoint: `POST /api/v1/restaurants/{pk}/menus/{menu_id}/items/`: Create a new menu

Endpoint: `GET /api/v1/restaurants/{pk}/menus/{menu_id}/items/`: List all the menu

### Retrieve/Update/Delete a Item of a menu

Endpoint: `GET /api/v1/restaurants/{pk}/menus/{menu_id}/items/{item_id}`: Get the Item details

Endpoint: `PUT /api/v1/restaurants/{pk}/menus/{menu_id}/items/{item_id}`: Update the Item details

Endpoint: `PATCH /api/v1/restaurants/{pk}/menus/{menu_id}/items/{item_id}`: Partial update the Item details

Endpoint: `DELETE /api/v1/restaurants/{pk}/menus/{menu_id}/items/{item_id}`: Delete the Item

## Order API

### Create or list orders

Endpoint: `GET /api/v1/orders/`: List all the orders

Response:

```json
[
  {
    "id": 17,
    "payment_status": "paid",
    "order_placed_by": 5,
    "payment_id": null
  },
  {
    "id": 16,
    "payment_status": "paid",
    "order_placed_by": 5,
    "payment_id": "14"
  }
]
```

Endpoint: `POST /api/v1/orders/`: Create new order

Request Body:

```json
{
  "items": [
    { "item": 1, "quantity": 2 },
    { "item": 6, "quantity": 1 }
  ]
}
```

Response:

```json
{
  "order_id": 20,
  "items": [
    {
      "item": 1,
      "quantity": 2
    },
    {
      "item": 6,
      "quantity": 1
    }
  ]
}
```

### Retrieve/Update/Delete order

Endpoint: `GET /api/v1/orders/{pk}/` : Get the Order

Endpoint: `PUT /api/v1/orders/{pk}/` : Update the Order

Endpoint: `PATCH /api/v1/orders/{pk}/` : Partial update the order

Endpoint: `DELETE /api/v1/orders/{pk}/` : Delete the order

## Payment API

### Steps to setup Stripe:
* Sign Up for Stripe and get your secrect key and put it in .env
* install stripe-cli to get stripe webhook working in local environment
* collect webhook secret key and put it into .env
* for more information: https://dashboard.stripe.com/test/webhooks/create?endpoint_location=local


### Create a new Payment

Endpoint: `POST /api/v1/payments/create/`: Create new order

Request body:

```json
{
  "order_id": 20
}
```

Response Body:

```json
{
  "order_id": 20,
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_a1yFLsTAVXWzlAtENKJzwa5mulwX1O9ewEwWBYYrGHX9ggGKdU6g2CUg7n#fidkdWxOYHwnPyd1blpxYHZxWjA0SmNOf0pGbX09aldzbm5GSkszQkRNX3VIVUFsNHN3RF92b29wfEEyNmZARE9Obl1tZHJNQk1oTm5KbDU0YlJgTTN%2FQmBjY19OcEYwXEFBMXRjQVJHNH9HNTUwf0hiTm1VQScpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"
}
```
