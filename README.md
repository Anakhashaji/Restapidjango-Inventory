# Inventory Management System API

This project is a backend API for a simple Inventory Management System built using Django Rest Framework. It supports CRUD operations on inventory items and includes JWT-based authentication for secure access.

## Features

- CRUD operations for inventory items
- JWT authentication
- PostgreSQL database
- Redis caching for improved performance
- Logging for debugging and monitoring
- Unit tests for API functionality

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/inventory-management-api.git
   cd inventory-management-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   - Create a new database named `inventory_db`
   - Update the database configuration in `inventory_management/settings.py` with your PostgreSQL credentials

5. Set up Redis:
   - Ensure Redis is running on localhost:6379
   - If your Redis configuration is different, update the CACHES setting in `inventory_management/settings.py`

6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token
- `GET /api/items/`: List all items
- `POST /api/items/`: Create a new item
- `GET /api/items/{id}/`: Retrieve a specific item
- `PUT /api/items/{id}/`: Update a specific item
- `DELETE /api/items/{id}/`: Delete a specific item

## Usage Examples

1. Obtain a JWT token:
   ```
   curl -X POST http://localhost:8000/api/token/ -d "username=yourusername&password=yourpassword"
   ```

2. List all items:
   ```
   curl -H "Authorization: Bearer <your_token>" http://localhost:8000/api/items/
   ```

3. Create a new item:
   ```
   curl -X POST -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d '{"name":"New Item","description":"Item description","quantity":10}' http://localhost:8000/api/items/
   ```

4. Retrieve a specific item:
   ```
   curl -H "Authorization: Bearer <your_token>" http://localhost:8000/api/items/1/
   ```

5. Update an item:
   ```
   curl -X PUT -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d '{"name":"Updated Item","description":"Updated description","quantity":15}' http://localhost:8000/api/items/1/
   ```

6. Delete an item:
   ```
   curl -X DELETE -H "Authorization: Bearer <your_token>" http://localhost:8000/api/items/1/
   ```

## Running Tests

To run the unit tests:

```
python manage.py test
```

## Logging

Logs are written to `debug.log` in the project root directory. You can configure the logging settings in `inventory_management/settings.py`.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.