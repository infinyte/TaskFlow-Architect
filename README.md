# TaskFlow Architect

*A modern, clean-architecture approach to task management built with Python and FastAPI*

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-brightgreen)](https://fastapi.tiangolo.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

TaskFlow Architect is a production-ready task management system that demonstrates modern software architecture principles. Built with Python and FastAPI, it showcases clean architecture, domain-driven design, and SOLID principles in a practical, real-world application.

### Key Features

- RESTful API with comprehensive documentation
- Clean Architecture implementation
- Domain-Driven Design patterns
- Asynchronous operations
- Type safety with Python type hints
- Comprehensive logging system
- In-memory repository with easy database integration
- Detailed API documentation with examples

## 🏗️ Architecture

The project follows Clean Architecture principles, organized in distinct layers:

```
taskflow_architect/
├── src/
│   ├── domain/          # Business logic and rules
│   ├── application/     # Use cases and DTOs
│   └── infrastructure/  # External interfaces
└── tests/              # Test suites
```

### Domain Layer
- Core business logic
- Business rules and validations
- Entity definitions
- Repository interfaces

### Application Layer
- Use case implementations
- DTOs (Data Transfer Objects)
- Service orchestration
- Business workflows

### Infrastructure Layer
- FastAPI implementation
- Repository implementations
- Logging system
- External service integrations

## 🛠️ Technical Stack

- **Python 3.9+**: Modern Python features and type hints
- **FastAPI**: High-performance web framework
- **Pydantic**: Data validation using Python type annotations
- **pytest**: Testing framework
- **uvicorn**: ASGI server implementation
- **Python Logging**: Built-in logging system

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/infinyte/taskflow-architect.git
cd taskflow-architect
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Starting the Server

Run the development server:
```bash
uvicorn src.main:app --reload --port 8000
```

### API Documentation

Access the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

| Method | Endpoint                          | Description                |
|--------|----------------------------------|----------------------------|
| POST   | /api/v1/tasks/                   | Create a new task         |
| GET    | /api/v1/tasks/                   | List all tasks            |
| GET    | /api/v1/tasks/{task_id}          | Get a specific task       |
| PATCH  | /api/v1/tasks/{task_id}          | Update a task             |
| POST   | /api/v1/tasks/{task_id}/assign   | Assign a task to a user   |

### Example Requests

Create a new task:
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Implement new feature",
       "description": "Add user authentication to the API",
       "assigned_to": "987fcdeb-51k2-12d3-a456-426614174000"
     }'
```

List all tasks:
```bash
curl "http://localhost:8000/api/v1/tasks/"
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_task_service.py
```

## 📖 API Documentation

The API documentation includes:

- Detailed request/response examples
- Interactive try-it-out functionality
- Schema validation information
- Error response examples
- Authentication details (if implemented)

### Example Response

```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Implement new feature",
    "description": "Add user authentication to the API",
    "status": "PENDING",
    "assigned_to": "987fcdeb-51k2-12d3-a456-426614174000",
    "created_at": "2024-01-16T10:00:00.000Z",
    "updated_at": "2024-01-16T10:00:00.000Z"
}
```

## 🔍 Error Handling

The API provides detailed error responses:

```json
{
    "detail": "Task not found",
    "type": "task_not_found",
    "status": 404
}
```

## 🛣️ Roadmap

Future improvements planned:

- [ ] Database integration (PostgreSQL)
- [ ] Authentication and authorization
- [ ] Docker containerization
- [ ] Rate limiting
- [ ] Response caching
- [ ] Advanced task features (deadlines, priorities)
- [ ] WebSocket notifications
- [ ] Task commenting system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please ensure your PR:
- Includes tests
- Updates documentation
- Follows the existing code style
- Includes a clear description of changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✨ Best Practices

- Clean Architecture principles
- SOLID design principles
- Domain-Driven Design
- Type safety
- Comprehensive testing
- Detailed documentation
- Error handling
- Logging
- API versioning

## 💡 Tips for Development

1. Use the interactive API documentation for testing
2. Check the examples in the documentation
3. Follow the existing code structure
4. Run tests before submitting changes
5. Keep the architecture layers separate

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)

## 🤔 Questions?

Feel free to:
1. Open an issue
2. Start a discussion
3. Submit a pull request
4. Contact the maintainers