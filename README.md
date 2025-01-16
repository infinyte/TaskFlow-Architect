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
git clone https://github.com/yourusername/taskflow-architect.git
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

### VS Code Setup

1. Install recommended VS Code extensions:
```json
{
    "recommendations": [
        "ms-python.python",                  // Python language support
        "ms-python.vscode-pylance",          // Python type checking
        "ms-python.black-formatter",         // Code formatting
        "njpwerner.autodocstring",           // Python docstring generation
        "kevinrose.vsc-python-indent",       // Smart Python indentation
        "littlefoxteam.vscode-python-test-adapter",  // Test Explorer UI
        "visualstudioexptteam.vscodeintellicode",    // AI-assisted development
        "christian-kohler.path-intellisense",        // Path autocompletion
        "aaron-bond.better-comments",                // Comment highlighting
        "ryanluker.vscode-coverage-gutters",        // Code coverage highlighting
        "yzhang.markdown-all-in-one",               // Markdown support
        "bierner.markdown-preview-github-styles",    // GitHub-style markdown
        "esbenp.prettier-vscode",                    // General code formatting
        "shardulm94.trailing-spaces",               // Highlight trailing spaces
        "streetsidesoftware.code-spell-checker"     // Spell checking
    ]
}
```

2. Create `.vscode/tasks.json` for common operations:
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start FastAPI Server",
            "type": "shell",
            "command": "${command:python.interpreterPath}",
            "args": [
                "-m",
                "uvicorn",
                "src.main:app",
                "--reload",
                "--port",
                "8000"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Run Tests",
            "type": "shell",
            "command": "${command:python.interpreterPath}",
            "args": [
                "-m",
                "pytest",
                "tests/",
                "-v"
            ],
            "group": "test",
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Run Tests with Coverage",
            "type": "shell",
            "command": "${command:python.interpreterPath}",
            "args": [
                "-m",
                "pytest",
                "tests/",
                "--cov=src",
                "--cov-report=html"
            ],
            "group": "test",
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Format Code",
            "type": "shell",
            "command": "${command:python.interpreterPath}",
            "args": [
                "-m",
                "black",
                "src/",
                "tests/"
            ],
            "group": "build"
        },
        {
            "label": "Install Dependencies",
            "type": "shell",
            "command": "${command:python.interpreterPath}",
            "args": [
                "-m",
                "pip",
                "install",
                "-r",
                "requirements.txt"
            ],
            "group": "none"
        }
    ]
}
```

3. Create `.vscode/snippets/python.json` for code snippets:
```json
{
    "FastAPI Route": {
        "prefix": "route",
        "body": [
            "@router.${1|get,post,put,patch,delete|}(",
            "    \"/${2:path}\",",
            "    response_model=${3:ResponseModel},",
            "    summary=\"${4:Summary}\",",
            "    response_description=\"${5:Response description}\"",
            ")",
            "async def ${6:function_name}(",
            "    ${7:parameters}",
            ") -> ${8:ReturnType}:",
            "    \"\"\"",
            "    ${9:Function description}",
            "    \"\"\"",
            "    try:",
            "        ${0:pass}",
            "    except Exception as error:",
            "        raise HTTPException(",
            "            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,",
            "            detail=str(error)",
            "        )"
        ],
        "description": "Create a FastAPI route"
    },
    "Domain Entity": {
        "prefix": "entity",
        "body": [
            "@dataclass",
            "class ${1:EntityName}:",
            "    \"\"\"",
            "    ${2:Entity description}",
            "    \"\"\"",
            "    id: UUID",
            "    ${3:field_name}: ${4:type}",
            "    created_at: datetime",
            "    updated_at: datetime",
            "",
            "    @classmethod",
            "    def create(cls, ${5:parameters}) -> \"${1:EntityName}\":",
            "        now = datetime.utcnow()",
            "        return cls(",
            "            id=uuid4(),",
            "            ${6:field_assignments},",
            "            created_at=now,",
            "            updated_at=now",
            "        )",
            "",
            "    def update(self, ${7:parameters}) -> None:",
            "        ${0:pass}"
        ],
        "description": "Create a domain entity"
    },
    "Repository Interface": {
        "prefix": "repo",
        "body": [
            "class ${1:EntityName}Repository(ABC):",
            "    @abstractmethod",
            "    async def save(self, ${2:entity}: ${3:EntityType}) -> None:",
            "        pass",
            "",
            "    @abstractmethod",
            "    async def find_by_id(self, id: UUID) -> Optional[${3:EntityType}]:",
            "        pass",
            "",
            "    @abstractmethod",
            "    async def find_all(self) -> List[${3:EntityType}]:",
            "        pass",
            "",
            "    @abstractmethod",
            "    async def delete(self, id: UUID) -> None:",
            "        pass$0"
        ],
        "description": "Create a repository interface"
    },
    "Service Class": {
        "prefix": "service",
        "body": [
            "class ${1:Name}Service:",
            "    def __init__(self, repository: ${2:RepositoryType}):",
            "        self.repository = repository",
            "",
            "    async def create_${3:entity}(self, ${4:parameters}) -> ${5:ReturnType}:",
            "        try:",
            "            ${0:pass}",
            "        except Exception as error:",
            "            raise ValueError(str(error))"
        ],
        "description": "Create a service class"
    },
    "Test Function": {
        "prefix": "test",
        "body": [
            "@pytest.mark.asyncio",
            "async def test_${1:function_name}():",
            "    # Arrange",
            "    ${2:arrangement}",
            "",
            "    # Act",
            "    ${3:action}",
            "",
            "    # Assert",
            "    ${0:assertion}"
        ],
        "description": "Create a test function"
    }
}
```

2. Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

3. Create `.vscode/launch.json` for debugging:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.main:app",
                "--reload",
                "--port",
                "8000"
            ],
            "jinja": true,
            "justMyCode": false
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Python: Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "-v",
                "tests/"
            ],
            "justMyCode": false
        }
    ]
}
```

### VS Code Usage

1. **Running the Server**:
   - Open the Debug panel (Ctrl+Shift+D / Cmd+Shift+D)
   - Select "Python: FastAPI" from the dropdown
   - Press F5 or click the green play button

2. **Debugging**:
   - Set breakpoints by clicking left of line numbers
   - Use the Debug toolbar to:
     - Continue (F5)
     - Step Over (F10)
     - Step Into (F11)
     - Step Out (Shift+F11)

3. **Running Tests**:
   - Option 1: Using Test Explorer
     - Open the Testing panel (Ctrl+Shift+T / Cmd+Shift+T)
     - Click Run All Tests or individual test buttons
   - Option 2: Using Debug Configuration
     - Select "Python: Tests" from debug dropdown
     - Press F5 to run with debugger

4. **Integrated Terminal**:
   - Open terminal: Ctrl+` / Cmd+`
   - Your virtual environment should activate automatically

5. **Code Navigation**:
   - Go to Definition: F12
   - Find All References: Shift+F12
   - Quick Fix: Ctrl+. / Cmd+.

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

## 🔧 VS Code Troubleshooting

Common VS Code issues and solutions:

1. **Python Interpreter Not Found**
   ```
   Problem: VS Code can't find Python interpreter
   Solution: 
   1. Cmd/Ctrl + Shift + P
   2. "Python: Select Interpreter"
   3. Choose the interpreter from your venv
   ```

2. **Debugger Not Working**
   ```
   Problem: Breakpoints not hitting
   Solution:
   1. Check if you're running with debugger (F5)
   2. Verify "justMyCode": false in launch.json
   3. Try deleting .pytest_cache directory
   ```

3. **Import Errors**
   ```
   Problem: "Import could not be resolved"
   Solution:
   1. Verify PYTHONPATH in settings.json
   2. Restart VS Code
   3. Rebuild IntelliSense cache:
      Cmd/Ctrl + Shift + P -> "Developer: Reload Window"
   ```

4. **Formatting Not Working**
   ```
   Problem: Code not formatting on save
   Solution:
   1. Check if black is installed
   2. Verify formatting settings in settings.json
   3. Try manual format: Shift + Alt + F
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