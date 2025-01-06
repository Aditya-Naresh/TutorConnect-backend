# TutorConnect Backend

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Endpoints](#endpoints)
- [Deployment](#deployment)

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

2. Create a [.env](http://_vscodecontentref_/1) file in the [tutorconnect](http://_vscodecontentref_/2) directory with the following content:

   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_USE_TLS=True
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-email-password
   SECRET_KEY=your-secret-key
   DEBUG=True
   FRONTEND=https://tutor-connect-ruddy.vercel.app
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

## Endpoints

### Authentication

- `POST /api/auth/login/` - Login a user
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/logout/` - Logout a user

### Users

- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Retrieve a user by ID
- `PUT /api/users/{id}/` - Update a user by ID
- `DELETE /api/users/{id}/` - Delete a user by ID

### Tutors

- `GET /api/tutors/` - List all tutors
- `GET /api/tutors/{id}/` - Retrieve a tutor by ID
- `POST /api/tutors/` - Create a new tutor
- `PUT /api/tutors/{id}/` - Update a tutor by ID
- `DELETE /api/tutors/{id}/` - Delete a tutor by ID

### Students

- `GET /api/students/` - List all students
- `GET /api/students/{id}/` - Retrieve a student by ID
- `POST /api/students/` - Create a new student
- `PUT /api/students/{id}/` - Update a student by ID
- `DELETE /api/students/{id}/` - Delete a student by ID

### Timeslots

- `GET /api/timeslots/` - List all timeslots
- `GET /api/timeslots/{id}/` - Retrieve a timeslot by ID
- `POST /api/timeslots/` - Create a new timeslot
- `PUT /api/timeslots/{id}/` - Update a timeslot by ID
- `DELETE /api/timeslots/{id}/` - Delete a timeslot by ID

### Chat

- `GET /api/chat/` - List all chat messages
- `POST /api/chat/` - Send a new chat message

### Notifications

- `GET /api/notifications/` - List all notifications
- `POST /api/notifications/` - Create a new notification

### Payments

- `POST /api/payments/` - Process a payment

## Deployment

The project is set up to be deployed using Docker and Azure VM. The deployment process is automated using GitHub Actions.

1. Ensure you have the necessary secrets set up in your GitHub repository:

   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
   - `VM_KEY`
   - `VM_IP`
   - `VM_USER`
   - `DB_HOST`
   - `DB_NAME`
   - `DB_PASSWORD`
   - `DB_USER`
   - `DEBUG`
   - `PUBLIC_KEY`
   - `RAZORPAY_SECRET_KEY`
   - `GOOGLE_AUTH_PASSWORD`
   - `FRONTEND`
   - `AZURE_KEY`
   - `AZURE_CONNECTION_STRING`

2. The deployment workflow is defined in [deploy.yml](http://_vscodecontentref_/3). It builds and pushes Docker images, then deploys them to the Azure VM.

3. To trigger a deployment, push changes to the `main` branch.

## License

This project is licensed under the MIT License.
