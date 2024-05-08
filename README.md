# Flask Authentication

<img src="screenshot.png">

Flask Authentication is a project that provides a basic authentication system built with Flask, a micro web framework for Python. It includes endpoints for user login and retrieving user information.


## Table of Contents

- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AppleBoiy/Flask-Auth.git
   ```

2. Navigate into the project directory:

   ```bash
   cd Flask-Auth
   ```

3. Build and run your Docker containers:

   ```bash
   make build
   ```
   
   Application should now be accessible at http://localhost:56733.

## API Endpoints

### View all users

```
GET /users
```

Response:

```json
[
   {
      "id": 1,
      "email": "user1@example.com",
      "confirmed_at": "2024-05-08T12:00:00"
   },
   {
      "id": 2,
      "email": "user2@example.com",
      "confirmed_at": "2024-05-08T12:00:00"
   }
]
```

### Search for a user by ID

```
GET /users/<user_id>
```

Response:

```json
{
   "id": 1,
   "email": "user1@example.com",
   "confirmed_at": "2024-05-08T12:00:00"
}
```

### Edit user information

```
PUT /users/<user_id>/edit
```

Request body (JSON):

```json
{
   "first_name": "John",
   "last_name": "Doe"
}
```

Response:

```json
{
   "message": "User information updated successfully"
}
```

## License

This project is licensed under the [MIT License](LICENSE).
