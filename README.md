# E-commerce website
- Link to the deployed website: https://akimskill.top/
- Video demonstration: https://drive.google.com/drive/folders/14WFjGIYY63oy_CbazkWk7xOFvJJe_H8G?usp=sharing
# Ecommerce Shop

Welcome to the Ecommerce Shop repository! This project is a full-stack application designed to provide a seamless online shopping experience. It encompasses functionalities for product browsing, user authentication, order management, and more.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Features

- **Product Management**: Browse and search for products with detailed descriptions and images.
- **User Authentication**: Secure user registration and login functionalities.
- **Shopping Cart**: Add products to the cart and manage quantities.
- **Order Processing**: Place orders and view order history.
- **Responsive Design**: Optimized for various devices and screen sizes.

## Technology Stack
- Django
- Django Rest Framework
- Django Allauth
- Celery
- Redis
- Nginx
- Gunicorn
- PostgreSQL
- Yandex Cloud

## Project Structure
```
Ecommerce-shop/
├── api/
│   ├── __init__.py
│   ├── apps.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── common/
│   └── views.py
│   
├── media/
│   ├── users_images
│   └── products_images     
│
├── orders/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── products/
│   ├── fixtures/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── static/
│   ├── css/
│   │   └── (static_css_files)
│   ├── js/
│   │   └── (static_js_files)
│   └── vendor/
│       └── (third_party_libraries)
│
├── store/
│   ├── __init__.py
│   ├── selery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .flake8
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt

```

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Akim-Edige/Ecommerce-shop.git
   cd Ecommerce-shop

2. **Set up a virtual environment (optional but recommended)**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate

2. **Set up a virtual environment** (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (for accessing the admin panel):

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.

## Usage

- **Admin Panel**: Access the Django admin interface at `http://127.0.0.1:8000/admin/` to manage products, orders, and users.
- **Product Browsing**: Navigate through the product listings
- **Shopping Cart**: Add desired products to your cart, adjust quantities, and proceed to checkout.
- **Order History**: After placing orders, view your order history and details in your user profile.


___
## API Endpoints

API endpoints are available by this link:
https://akimskill.top/api/schema/swagger-ui/
___ 
### User Authentication and management
- **POST** -  /api/users/create/: _Create new user with email verification_
- **POST** -/api-token-auth/: _Log in with email and password to obtain a token._
- **PUT** - /api/users/{id}/: _Update all fields of the particular user by id_
- **PATCH** - /api/users/{id}/: _Update particular fields of the user by id_
- **DELETE** - /api/users/{id}/: _Delete particular user by id_

### Basket management
- **GET** -  /api/basket/create/: _Get products info, total count and total sum of the authenticated user_
- **POST** -/api/basket/add/: _Add particular product by id to the authenticated user_
- **POST** - /api/basket/remove/: _Remove 1 unit of particular product by id or delete from basket if there is single quantity_

### Products management
- **GET** -  /api/products/: _Get all products info paginated by 3, available for anyone_
- **POST** -/api/products/: _Create a new product, admin user authentication is required_
- **GET** - /api/products/{id}/: _Get particular product info by id, available for anyone_
- **PUT** - /api/products/{id}/: _Update all fields of the particular product by id, admin user authentication is required_
- **PATCH** - /api/products/{id}/: _Update particular fields of the product by id, admin user authentication is required_
- **DELETE** - /api/products/{id}/: _Delete particular product by id, admin user authentication is required_

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
