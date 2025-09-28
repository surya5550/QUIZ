#  Quiz API (Django + DRF + JWT)

This is a Quiz Management API built with **Django Rest Framework (DRF)** and **JWT Authentication**.  
It allows users to register, log in, take quizzes, and submit answers.  
Admin users can manage categories, quizzes, and questions.

##  Features

- User and Admin registration
- JWT-based authentication (login & refresh tokens)
- Manage Categories, Quizzes, and Questions
- Submit quiz answers and track submissions
- REST API endpoints with CRUD operations
- Organized using `ViewSets` and `DefaultRouter`


##  Installation & Setup

1. **Clone the repository**
   
   git clone https://github.com/surya5550/QUIZ.git
   cd QUIZ

## Create virtual environment

python -m venv venv
source venv/Scripts/activate   # Windows
source venv/bin/activate       # Linux/Mac

## Install dependencies

pip install -r requirements.txt

## Run migrations

python manage.py makemigrations
python manage.py migrate

## Run the server

python manage.py runserver

## The project uses JWT Authentication.

Get token:

POST /api/auth/token/
{
  "username": "your_username",
  "password": "your_password"
}

Refresh token:

POST /api/auth/token/refresh/

## API Endpoints

- Auth

POST /api/auth/register/ → Register user

POST /api/auth/register/admin/ → Register admin

POST /api/auth/token/ → Get JWT token

POST /api/auth/token/refresh/ → Refresh JWT token

- Categories

GET /api/categories/

POST /api/categories/

PUT /api/categories/<id>/

DELETE /api/categories/<id>/

- Quizzes

GET /api/quizzes/

POST /api/quizzes/

PUT /api/quizzes/<id>/

DELETE /api/quizzes/<id>/

- Questions

GET /api/questions/

POST /api/questions/

PUT /api/questions/<id>/

DELETE /api/questions/<id>/

- Submissions

POST /api/submissions/

## Tech Stack
 
Python 3.12.10

Django 5.2.6

Django Rest Framework 3.16.1

SimpleJWT (Authentication) 5.5.1
