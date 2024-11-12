# Mail-Sending-Project (Master branch)

This project is a Flask-based REST API designed to register users with unique email addresses and automatically send confirmation emails via the Gmail API upon successful registration. It provides a simple way to handle user registration and confirmation email functionality through a RESTful API.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Endpoints](#endpoints)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

The Mail-Sending Project is built with Flask to create a REST API that allows users to register with a unique email address. Upon successful registration, a confirmation email is automatically sent using the Gmail API. The project also allows finding registered users by their email addresses.

## Features

- **User Registration**: Registers users with unique email addresses.
- **Email Confirmation**: Sends a confirmation email upon successful registration.
- **User Lookup**: Finds and retrieves user information based on email.

## Endpoints

The API includes the following endpoints:

1. **Register User**: Registers a new user with a unique email and sends a confirmation email.
2. **Find User**: Retrieves information about a registered user based on their email.

## Installation

### Prerequisites

- Docker
- Gmail API credentials

### Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/mail-sending-project.git
   cd mail-sending-project
   ```
2. Add Gmail API Credentials

- Place your Gmail API credentials in a file named `credentials.json` in the project root directory.

3. Run the Project

```bash
docker-compose up --build
```

## Usage

Once the server is running, you can use the following endpoints:

1. **Register User**: POST request to `/register` with JSON payload containing user details (e.g., `{"email": "user@example.com"}`).
    - Sends a confirmation email upon successful registration.

2. **Find User**: GET request to `/find-user?email=user@example.com` to retrieve user information by email.


