# TutorConnect Backend

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)

## Introduction

TutorConnect is a platform that connects tutors with students for online learning sessions. This repository contains the backend code for the TutorConnect application.

## Features

- User authentication and authorization
- Tutor and student management
- Scheduling and managing timeslots
- Real-time chat and notifications
- Video call integration
- Payment processing with Razorpay

## Technologies

- Python
- Django
- Django Rest Framework
- Celery
- Redis
- Docker
- PostgreSQL

## Setup

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/tutorconnect-backend.git
   cd tutorconnect-backend
   ```

2. Create a [.env] file in the [tutorconnect] directory with the following content:

   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_USE_TLS=True
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-email-password
   SECRET_KEY=your-secret-key
   DEBUG=True
   FRONTEND=your-local-frontend-link
   AZURE_KEY=your-azure-key
   AZURE_ACCOUNT_NAME=your-azure-account-name
   AZURE_CONNECTION_STRING=your-azure-connection-string
   RAZORPAY_SECRET_KEY=your-razorpay-secret-key
   PUBLIC_KEY=your-public-key
   ```

3. Build and run the Docker containers:

   ```sh
   docker-compose up --build
   ```

4. Run database migrations:

   ```sh
   docker exec tutorconnect-backend-web python manage.py migrate
   ```

5. Create a superuser:

   ```sh
   docker exec tutorconnect-backend-web python manage.py createsuperuser
   ```

6. Access the application at `http://localhost:8000`.

