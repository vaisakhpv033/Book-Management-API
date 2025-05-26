# Book Management API

This project is a Book Management API that allows users to manage a collection of books. It provides endpoints for creating, reading, updating, and deleting books.

## Setup Instructions

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```
Replace `<repository_url>` with the actual URL of the repository and `<repository_directory>` with the name of the directory created after cloning.

### 2. Set Up a Python Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

*   **On macOS and Linux:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

*   **On Windows:**

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 3. Install Dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

The application uses a `.env` file to manage sensitive configuration and environment-specific settings. This file should be placed in the `BookManagement` project root directory (the same directory where `manage.py` is located).

Create a file named `.env` in the `BookManagement` project root directory and add the following environment variables.

**Required Environment Variables:**

*   `SECRET_KEY`: A strong, unique secret key for your Django application.
*   `DEBUG`: Set to `True` for development or `False` for production.
*   `DB_NAME`: The name of your PostgreSQL database.
*   `DB_USER`: The username for your PostgreSQL database.
*   `DB_PASSWORD`: The password for your PostgreSQL database user.
*   `DB_HOST`: The host where your PostgreSQL database is running (e.g., `localhost`).
*   `DB_PORT`: The port on which your PostgreSQL database is listening (e.g., `5432`. This is optional if using the default PostgreSQL port).

**Example `.env` content:**

```env
# .env.example - Copy this to .env in the BookManagement project root directory and fill in your actual values

SECRET_KEY="your_strong_secret_key_here"
DEBUG=True

DB_NAME="bookmanagement_db"
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"
DB_HOST="localhost"
DB_PORT="5432"
```

**Note:** Ensure your PostgreSQL server is running and the specified database (`DB_NAME`) and user (`DB_USER`) are created with appropriate permissions.

### 5. Run Database Migrations

Apply the database migrations to set up your database schema:

```bash
python manage.py migrate
```

### 6. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The API should now be accessible at `http://127.0.0.1:8000/` by default.

## API Endpoints

This section outlines the available API endpoints.

### Accounts API Endpoints

Base path: `/api/v1/accounts/`

*   **`/login/`**
    *   **Method:** `POST`
    *   **Description:** Obtain JWT access and refresh tokens.
    *   **Authentication Required:** No
*   **`/token/refresh/`**
    *   **Method:** `POST`
    *   **Description:** Refresh JWT access token using a valid refresh token.
    *   **Authentication Required:** No (but requires a valid refresh token)
*   **`/register/`**
    *   **Method:** `POST`
    *   **Description:** Register a new user.
    *   **Authentication Required:** No
*   **`/profile/`**
    *   **Methods:** `GET`, `PUT`, `PATCH`
    *   **Description:** View and update user profile.
    *   **Authentication Required:** Yes

### Books API Endpoints

Base path: `/api/v1/`

The following endpoints are managed by a Django Rest Framework `DefaultRouter`.

*   **`/books/`**
    *   **Method:** `GET`
    *   **Description:** List all books.
    *   **Authentication Required:** Yes
    *   **Method:** `POST`
    *   **Description:** Create a new book.
    *   **Authentication Required:** Yes
*   **`/books/{id}/`**
    *   **Method:** `GET`
    *   **Description:** Retrieve a specific book by its ID.
    *   **Authentication Required:** Yes
    *   **Method:** `PUT`
    *   **Description:** Update a specific book by its ID.
    *   **Authentication Required:** Yes
    *   **Method:** `PATCH`
    *   **Description:** Partially update a specific book by its ID.
    *   **Authentication Required:** Yes
    *   **Method:** `DELETE`
    *   **Description:** Delete a specific book by its ID.
    *   **Authentication Required:** Yes
*   **`/reading-list/`**
    *   **Method:** `GET`
    *   **Description:** List items in the user's reading list.
    *   **Authentication Required:** Yes
    *   **Method:** `POST`
    *   **Description:** Add a book to the authenticated user's reading list.
    *   **Authentication Required:** Yes
*   **`/reading-list/{id}/`**
    *   **Method:** `GET`
    *   **Description:** Retrieve a specific item from the reading list by its ID.
    *   **Authentication Required:** Yes
    *   **Method:** `DELETE`
    *   **Description:** Remove a book from the reading list by its ID.
    *   **Authentication Required:** Yes
*   **`/authors/`**
    *   **Method:** `GET`
    *   **Description:** List all authors.
    *   **Authentication Required:** Yes
    *   **Method:** `POST`
    *   **Description:** Create a new author.
    *   **Authentication Required:** Yes
*   **`/authors/{id}/`**
    *   **Method:** `GET`
    *   **Description:** Retrieve a specific author by their ID.
    *   **Authentication Required:** Yes
    *   **Method:** `PUT`
    *   **Description:** Update a specific author by their ID.
    *   **Authentication Required:** Yes
    *   **Method:** `PATCH`
    *   **Description:** Partially update a specific author by their ID.
    *   **Authentication Required:** Yes
    *   **Method:** `DELETE`
    *   **Description:** Delete a specific author by their ID.
    *   **Authentication Required:** Yes
*   **`/genres/`**
    *   **Method:** `GET`
    *   **Description:** List all genres.
    *   **Authentication Required:** Yes
    *   **Method:** `POST`
    *   **Description:** Create a new genre.
    *   **Authentication Required:** Yes
*   **`/genres/{id}/`**
    *   **Method:** `GET`
    *   **Description:** Retrieve a specific genre by its ID.
    *   **Authentication Required:** Yes
    *   **Method:** `PUT`
    *   **Description:** Update a specific genre by its ID.
    *   **Authentication Required:** Yes
    *   **Method:** `PATCH`
    *   **Description:** Partially update a specific genre by its ID.
    *   **Authentication Required:** Yes
    *   **Method:** `DELETE`
    *   **Description:** Delete a specific genre by its ID.
    *   **Authentication Required:** Yes

## Authentication

This API uses JWT (JSON Web Token) authentication, implemented with the `djangorestframework-simplejwt` package.

To access protected endpoints, clients must include an `Authorization` header in their requests with a valid access token:

```
Authorization: Bearer <access_token>
```

You can obtain and refresh your tokens using the following endpoints:

*   **Obtain Tokens:** `/api/v1/accounts/login/`
*   **Refresh Access Token:** `/api/v1/accounts/token/refresh/`

Please refer to the "API Endpoints" section for more details on these and other account-related endpoints.
