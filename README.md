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

- **POST /login**: User login.
- **POST /logout**: User logout.
- **POST /register**: Create new user.
- **GET /users**: Retrieve all users.

## License

This project is licensed under the [MIT License](LICENSE).
