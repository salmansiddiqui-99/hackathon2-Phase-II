# Todo App Backend API

This is the FastAPI backend for the Todo Full-Stack Web Application, deployed on Hugging Face Spaces.

## Features

- RESTful API endpoints for todo management
- JWT-based authentication
- Multi-user data isolation
- PostgreSQL database integration (Neon)
- CORS enabled for frontend integration

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT with Better Auth
- **Deployment**: Docker on Hugging Face Spaces

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and receive JWT token
- `POST /api/auth/logout` - Logout (invalidate token)

### Tasks

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task
- `PATCH /api/tasks/{task_id}/toggle` - Toggle task completion status

## Environment Variables

Configure these in Hugging Face Spaces Settings → Repository secrets:

- `DATABASE_URL`: PostgreSQL connection string (Neon)
- `BETTER_AUTH_SECRET`: Secret key for JWT token generation

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your values

# Run development server
uvicorn src.main:app --reload --port 8000
```

## Deployment

This backend is configured for deployment on Hugging Face Spaces using Docker.

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed deployment instructions.

## Documentation

Once deployed, API documentation is available at:

- Swagger UI: `https://YOUR-SPACE-URL/docs`
- ReDoc: `https://YOUR-SPACE-URL/redoc`

## Security

- All passwords are hashed using bcrypt
- JWT tokens expire after 24 hours
- CORS is configured to only allow requests from authorized frontend domains
- SQL injection protection via SQLModel/SQLAlchemy
- Input validation using Pydantic models

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue in the GitHub repository.
