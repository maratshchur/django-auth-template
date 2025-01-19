# Django REST API for User Authentication and Authorization

This project is a Django-based REST API for user authentication and authorization. It supports user registration, authentication, access token refreshing, logout, and personal information retrieval/update. The system is designed with security and scalability in mind, leveraging **Django REST Framework**, **PyJWT**, and **django-constance** for flexibility in token management.

## Features

1. **User Registration**  
   Allows users to register with an email and password.
   - **Endpoint**: `/api/register/`
   - **Method**: `POST`
   - **Response**: Returns the user ID and email upon successful registration.
   - Example:
     ```bash
     curl -X POST http://localhost:8000/api/register/ -d '{"password": "password", "email": "user@example.com"}' -H "Content-Type: application/json"
     ```

2. **User Authentication**  
   Allows users to log in and receive a pair of tokens: an **Access Token** (JWT) and a **Refresh Token** (UUID stored in the database).
   - **Endpoint**: `/api/login/`
   - **Method**: `POST`
   - **Response**: Returns an `access_token` and a `refresh_token`.
   - Example:
     ```bash
     curl -X POST http://localhost:8000/api/login/ -d '{"email": "user@example.com", "password": "password"}' -H "Content-Type: application/json"
     ```

3. **Access Token Refresh**  
   Allows users to refresh their Access Token by providing a valid Refresh Token. A new pair of tokens is issued.
   - **Endpoint**: `/api/refresh/`
   - **Method**: `POST`
   - **Response**: Returns a new `access_token` and `refresh_token`.
   - Example:
     ```bash
     curl -X POST http://localhost:8000/api/refresh/ -d '{"refresh_token": "d952527b-caef-452c-8c93-1100214f82e5"}' -H "Content-Type: application/json"
     ```

4. **Logout**  
   Invalidates the provided Refresh Token, logging the user out.
   - **Endpoint**: `/api/logout/`
   - **Method**: `POST`
   - **Response**: Confirmation message indicating successful logout.
   - Example:
     ```bash
     curl -X POST http://localhost:8000/api/logout/ -d '{"refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"}' -H "Content-Type: application/json"
     ```

5. **Retrieve Personal Information**  
   Authenticated users can retrieve their personal profile details.
   - **Endpoint**: `/api/me/`
   - **Method**: `GET`
   - **Header**: Provide the valid `Authorization: Bearer <access_token>`.
   - Response: Returns user ID, username, and email.
   - Example:
     ```bash
     curl -X GET http://localhost:8000/api/me/ -H "Authorization: Bearer <access_token>"
     ```

6. **Update Personal Information**  
   Authenticated users can update their personal profile details.
   - **Endpoint**: `/api/me/`
   - **Method**: `PUT`
   - **Header**: Provide the valid `Authorization: Bearer <access_token>`.
   - **Body**: User fields to update (e.g., `username` or `email`).
   - Example:
     ```bash
     curl -X PUT http://localhost:8000/api/me/ -d '{"username": "John Smith"}' -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>"
     ```

---

## Technical Details

### 1. **Access and Refresh Tokens**
- **Access Token**: A short-lived JWT (30 seconds by default) used for authentication purposes. It is verified using the `PyJWT` library without database calls.
- **Refresh Token**: A UUID stored in the database with a default lifespan of 30 days. It is used to generate new Access Tokens when they expire.

### 2. **Token Management**
- The **django-constance** module is used to manage token lifetimes dynamically via the Django Admin interface.  
  Admin URL: `/admin/constance/config/`

### 3. **Security**
- Passwords are hashed using Django's `AbstractBaseUser` mechanism.
- Refresh Tokens are securely stored in the database and invalidated during logout.

### 4. **API Documentation**
- The browsable API interface provides user-friendly documentation for all endpoints. Accessible via the `/api/` URL.

### 5. **Testing**
- Unit and integration tests are included to ensure the API behaves as expected.
- Test cases cover user registration, login, token refresh, logout, and profile updates.

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/auth-system.git
   cd auth-system
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the API**:
   - API Base URL: `http://localhost:8000/api/`
   - Admin Panel: `http://localhost:8000/admin/`

---

<!-- ## Deployment

The application can be deployed on **Heroku** or similar platforms. Below are the basic steps for deploying to Heroku:

1. Install the Heroku CLI and log in:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create
   ```

3. Push the code to Heroku:
   ```bash
   git push heroku main
   ```

4. Set environment variables in Heroku for Django settings:
   ```bash
   heroku config:set DEBUG=False SECRET_KEY='<your-secret-key>' ALLOWED_HOSTS='*'
   ```

5. Run migrations on Heroku:
   ```bash
   heroku run python manage.py migrate
   ```

--- -->

## Configuration

The following token lifetimes can be modified via the Django Admin interface:
- Access Token Lifetime: `30 seconds` (default)
- Refresh Token Lifetime: `30 days` (default)

Navigate to `/admin/constance/config/` to update these settings.

---

## API Demo Links

- **Deployed API**: [Demo API](https://auth-temp-48821ad5a163.herokuapp.com/api/)
- **Admin Panel**: [Admin Panel](https://auth-temp-48821ad5a163.herokuapp.com/admin/)

---

## Repository

The source code is publicly available on GitHub: [GitHub Repository](https://github.com/maratshchur/django-auth-template)

---