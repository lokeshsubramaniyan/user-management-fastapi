# User Management API

A comprehensive FastAPI application for user management with JWT authentication and credential management capabilities. This project provides a secure, scalable backend API for managing users and their associated credentials.

## 🚀 Features

### User Management
- **User Registration & Authentication**: Secure user registration with password hashing
- **JWT Token Authentication**: Stateless authentication using JWT tokens
- **User CRUD Operations**: Complete Create, Read, Update, Delete operations
- **Authorization**: Role-based access control ensuring users can only access their own data
- **Password Validation**: Enforces password complexity requirements

### Credential Management
- **Credential Storage**: Secure storage of user credentials (passwords, usernames, URLs)
- **Credential CRUD Operations**: Full lifecycle management of user credentials
- **User-specific Credentials**: Each user can manage their own credential collection
- **Soft Delete**: Credentials are marked as deleted rather than permanently removed

### Technical Features
- **MongoDB Integration**: NoSQL database for flexible data storage
- **Pydantic Validation**: Robust data validation and serialization
- **CORS Support**: Cross-origin resource sharing enabled
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Error Handling**: Proper HTTP status codes and error messages
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 📋 Prerequisites

- Python 3.8+
- MongoDB (local or MongoDB Atlas)
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd user-management
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory with the following variables:
   ```env
   MONGO_URI=your_mongodb_connection_string
   MONGO_DB_NAME=user_management_db
   SECRET_KEY=your_secret_key_for_jwt
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:
- **Interactive API Documentation**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## 🔐 API Endpoints

### Authentication
- `POST /api/users/login` - User login
- `GET /api/users/me` - Get current user info

### User Management
- `POST /api/users` - Create new user
- `GET /api/users` - Get all users (with filtering and sorting)
- `GET /api/users/{id}/user` - Get user by ID
- `PUT /api/users/{id}/update` - Update user
- `DELETE /api/users/{id}/delete` - Delete user

### Credential Management
- `POST /api/credential/{user_id}/user` - Create credential
- `GET /api/credential/{user_id}/user` - Get all credentials for user
- `GET /api/credential/{user_id}/user/{credential_id}` - Get specific credential
- `PUT /api/credential/{user_id}/user/{credential_id}/update` - Update credential
- `DELETE /api/credential/{user_id}/user/{credential_id}/delete` - Delete credential

## 🏗️ Project Structure

```
user-management/
├── app/
│   ├── api/                    # API route handlers
│   │   ├── users.py           # User endpoints
│   │   └── credential.py      # Credential endpoints
│   ├── auth/                  # Authentication & authorization
│   │   ├── auth_bearer.py     # JWT bearer token handling
│   │   └── security.py        # Security utilities
│   ├── constants/             # Application constants
│   │   └── constants.py
│   ├── crud/                  # Database operations
│   │   ├── user_crud.py       # User CRUD operations
│   │   └── credential_crud.py # Credential CRUD operations
│   ├── models/                # Data models
│   │   ├── user.py           # User data models
│   │   └── credential.py     # Credential data models
│   ├── schemas/               # Pydantic schemas
│   │   ├── userSchema.py     # User validation schemas
│   │   ├── credentialSchema.py # Credential validation schemas
│   │   └── token.py          # Token schemas
│   ├── services/              # Business logic
│   │   ├── user_service.py   # User business logic
│   │   └── credential_service.py # Credential business logic
│   ├── utilities/             # Utility functions
│   │   └── util.py
│   ├── db_config.py          # Database configuration
│   └── main.py               # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

## 🔧 Usage Examples

### 1. User Registration
```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123",
    "name": "John Doe",
    "email_id": "john@example.com",
    "date_of_birth": "1990-01-01"
  }'
```

### 2. User Login
```bash
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123"
  }'
```

### 3. Create Credential (with JWT token)
```bash
curl -X POST "http://localhost:8000/api/credential/{user_id}/user" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Gmail Account",
    "username": "john@gmail.com",
    "password": "gmail_password",
    "url": "https://gmail.com",
    "notes": "Personal email account"
  }'
```

### 4. Get User Credentials
```bash
curl -X GET "http://localhost:8000/api/credential/{user_id}/user" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔒 Security Features

- **Password Hashing**: All passwords are hashed using bcrypt
- **JWT Authentication**: Secure token-based authentication
- **Authorization**: Users can only access their own data
- **Input Validation**: Comprehensive data validation using Pydantic
- **CORS Protection**: Configurable cross-origin resource sharing

## 🧪 Testing

The project includes comprehensive error handling and validation. You can test the API using:

1. **Interactive Documentation**: Visit `http://localhost:8000/docs`
2. **Postman Collection**: Import the provided Postman collection
3. **cURL Commands**: Use the examples provided above

## 📝 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `MONGO_URI` | MongoDB connection string | Yes | - |
| `MONGO_DB_NAME` | Database name | Yes | `user_management_db` |
| `SECRET_KEY` | JWT secret key | Yes | - |
| `ALGORITHM` | JWT algorithm | No | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | No | `30` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the API documentation at `http://localhost:8000/docs`
2. Review the error logs in the console
3. Ensure all environment variables are properly configured
4. Verify MongoDB connection is working

## 🔄 Version History

- **v1.0.0**: Initial release with user and credential management
- Added JWT authentication
- Implemented CRUD operations for users and credentials
- Added comprehensive API documentation 