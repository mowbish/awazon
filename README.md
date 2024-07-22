### Directory Structure

```plaintext
.
├───apps
│   ├───core
│   │   └───migrations
│   ├───products
│   │   ├───api
│   │   │   └───v1
│   │   └───migrations
│   └───users
│   │   ├───api
│   │   │   └───v1
│   │   └───migrations
└───config
```

# 🛍️ **Awazon Product API**

Welcome to the Awazon Product API! This project is a Django application designed to scrape and manage product information from Amazon. It utilizes Docker for containerization and deployment.

## 📚 **Table of Contents**

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Environment Variables](#-environment-variables)
- [API Endpoints](#-api-endpoints)
- [Database Migrations](#-database-migrations)
- [Creating a Superuser](#-creating-a-superuser)
- [Testing](#-testing)
- [License](#-license)
- [Contributing](#-contributing)

## ✨ **Features**

- Scrape product data from Amazon using ASIN codes.
- Cache product data for improved performance.
- RESTful API to retrieve product information.
- Fully containerized with Docker.

## 📋 **Requirements**

- Docker 🐳
- Docker Compose 🐙

## 🚀 **Installation**

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/awazon-product-api.git
    cd awazon-product-api
    ```

2. **Create a `.env` file:**

    ```env
    DEBUG=1
    SECRET_KEY=your_secret_key
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    DATABASE_URL=postgres://your_database_user:your_database_password@db:5432/your_database_name
    ```

3. **Build and run the Docker containers:**

    ```bash
    docker-compose build
    docker-compose up
    ```

## 🏃 **Running the Application**

Once the Docker containers are up and running, the application will be accessible at `http://localhost:8000`.

## 🌐 **Environment Variables**

Make sure to set up the following environment variables in your `.env` file:

- `DEBUG`: Set to `1` for development mode.
- `SECRET_KEY`: A secret key for your Django application.
- `DJANGO_ALLOWED_HOSTS`: A list of allowed hosts.
- `DATABASE_URL`: The database connection URL.

## 📡 **API Endpoints**

### Users

- **Create User:**
  ```
  url:
  POST /api/v1/users/
  ```
  ```
  Body:
  {
    "username": "username",
    "email": "user@example.com",
    "password": "string",
    "is_suspended": true,
    "gender": "MALE",
    "auth_level": 1,
    "phone_number": "string",
    "birthday": "2024-07-22"
  }
  ```

  Obtain a new token pair (access and refresh tokens).

- **Token Obtain Pair:**
  
  ```
  url:
  POST /api/token/
  ```
  ```
  Body:
  {
    "username": "username",
    "password": "string",
  }
  ```
  Obtain a new token pair (access and refresh tokens).

- **Token Refresh:**
  
  ```
  url:
  POST /api/token/refresh/
  ```
  ```
  body:
  {
    "access_token": "ACCESS_TOKEN"
  }
  ```
  Refresh the access token.

- **User Profile:**
  
  ```
  GET /api/v1/users/profile/
  PUT /api/v1/users/profile/
  ```

  Retrieve or update the authenticated user's profile.

### Products (Amazon)✅

- **Retrieve Product Details:**
  
  ```
  GET /api/v1/products/{asin}/
  ```

  Retrieves the details of a product using its ASIN code(for example: **B0CGC4PJ3Q**). If the product is not found in the cache or database, it scrapes the data from Amazon.

## 🔄 **Database Migrations**

To apply the database migrations, run the following command:

```bash
docker-compose exec web python manage.py migrate
```

## 🔑 **Creating a Superuser**

To create a superuser for accessing the Django admin, run:

```bash
docker-compose exec web python manage.py createsuperuser
```

## 🧪 **Testing**

You can run the tests using the following command:

```bash
docker-compose exec web python manage.py test
```