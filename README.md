# REST APIs for blogging site using DRF

## Features

- JWT Authentication
- CRUD operations
- Comment-reply system
- Paginated Responses
- Admin Panel

## Tech Stack

- Django Rest Framework

- PostgrSQL Database

- AWS S3

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`: Django secret key

`DEBUG`: Indicate whether the application is running in development (True) or production (False) mode

`APP_HOST`: Allowed host URL

`ACCESS_TOKEN_LIFETIME_WEEKS`: Access Token lifetime in weeks.

`ACCESS_TOKEN_LIFETIME_DAYS`: Access Token lifetime in days.

`ACCESS_TOKEN_LIFETIME_HOURS`: Access Token lifetime in hours.

`ACCESS_TOKEN_LIFETIME_MINUTES`: Access Token lifetime in minutes.

`REFRESH ACCESS_TOKEN_LIFETIME_WEEKS`: Refresh Token lifetime in weeks.

`REFRESH ACCESS_TOKEN_LIFETIME_DAYS`: Refresh Token lifetime in days.

`REFRESH ACCESS_TOKEN_LIFETIME_HOURS`: Refresh Token lifetime in hours.

`REFRESH ACCESS_TOKEN_LIFETIME_MINUTES`: Refresh Token lifetime in minutes.

`AWS_ACCESS_KEY_ID`: Your AWS access key Id.

`AWS_SECRET_ACCESS_KEY`: Your AWS access key.

`AWS_STORAGE_BUCKET_NAME`: Name of the S3 bucket where you want to host the static files.

`AWS_S3_REGION_NAME`: AWS region name. For example, `ap-south-1`.

## Run Locally

### For windows

Clone the project

```bash
  git clone https://github.com/helios274/BlogAPI.git
```

Go to the project directory

```bash
  cd BlogAPI
```

Create a virtual environment

```bash
  python -m venv .venv
```

Activate virtual environment

```bash
  .venv\Scripts\activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run server

```bash
  python manage.py runserver
```
