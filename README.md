# Simple CRUD Application with PostgreSQL

A production-ready Spring Boot application with PostgreSQL database, Docker containerization, and comprehensive CRUD operations.

## Features

- **Complete CRUD Operations**: Create, Read, Update, Delete users
- **PostgreSQL Integration**: Using HikariCP connection pooling
- **Docker & Docker Compose**: Multi-container deployment with health checks
- **Native Image Build**: Optimized GraalVM native compilation
- **Validation**: Input validation with proper error handling
- **Health Checks**: Actuator endpoints for monitoring
- **Production Ready**: Proper error handling, validation, and security

## Tech Stack

- **Backend**: Spring Boot 3.5.7
- **Database**: PostgreSQL
- **Language**: Java 25
- **Build Tool**: Gradle
- **Runtime**: GraalVM Native Image
- **Containerization**: Docker & Docker Compose
- **Connection Pool**: HikariCP
- **Validation**: Bean Validation (Jakarta Validation)

## Project Structure

```
src/
├── main/
│   ├── java/com/sapta/simplecurd/
│   │   ├── entity/          # JPA entities
│   │   ├── repository/      # Data repositories
│   │   ├── service/         # Business logic
│   │   └── controller/      # REST controllers
│   └── resources/
│       └── application.properties  # Configuration
├── test/                    # Unit & Integration tests
build.gradle.kts            # Build configuration
Dockerfile                  # Multi-stage native build
docker-compose.yml          # Docker orchestration
README.md                   # This file
```

## API Endpoints

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/users` | Get all users |
| GET    | `/api/users/{id}` | Get user by ID |
| POST   | `/api/users` | Create new user |
| PUT    | `/api/users/{id}` | Update existing user |
| DELETE | `/api/users/{id}` | Delete user |

### Health & Monitoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/actuator/health` | Health check |
| GET    | `/actuator/info` | Application info |

### Request/Response Format

**Create/Update User:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "address": "123 Main St"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "address": "123 Main St"
}
```

## Prerequisites

- Docker & Docker Compose
- Java 25 (for local development)
- GraalVM (for native builds)

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd simplecurd
```

### 2. Build and Run with Docker Compose

```bash
# Build and start both PostgreSQL and application
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

The application will be available at `http://localhost:8080`

### 3. Alternative: Local Development

```bash
# Run PostgreSQL with Docker
docker run --name simplecurd-postgres -e POSTGRES_DB=simplecurd_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15

# Build the application
./gradlew build

# Run the application
./gradlew bootRun
```

## Configuration

### Database Configuration

The application is configured to connect to PostgreSQL with the following settings:

- **URL**: `jdbc:postgresql://localhost:5432/simplecurd_db`
- **Username**: `postgres`
- **Password**: `postgres`
- **Driver**: `org.postgresql.Driver`

### HikariCP Connection Pool

- **Pool Name**: `HikariPool`
- **Max Pool Size**: `20`
- **Min Idle**: `5`
- **Connection Timeout**: `30 seconds`
- **Max Lifetime**: `10 minutes`
- **Idle Timeout**: `5 minutes`

### Docker Compose Services

- **postgres**: PostgreSQL 15 with health check
- **app**: Spring Boot application with native image
- **Health Checks**: Both services have health checks configured
- **Dependencies**: App waits for PostgreSQL to be healthy

## Docker Images

### Multi-stage Dockerfile

The Dockerfile implements a multi-stage build process:

1. **Builder Stage**: Uses GraalVM native image to compile the application
2. **Runtime Stage**: Creates minimal runtime image with the native executable

### Docker Compose Health Checks

- **PostgreSQL**: Uses `pg_isready` to check database readiness
- **Application**: Uses `/actuator/health` endpoint to verify application health
- **Dependencies**: Application starts only after PostgreSQL is healthy

## Testing

### API Testing

A comprehensive Python test script is included:

```bash
# Run the test script
python test_crud_api.py
```

The test script:
- Creates 10 users with unique data
- Tests all CRUD operations
- Verifies health endpoints
- Tests error cases
- Prints detailed request/response information

### Manual Testing

You can also test the API manually using curl:

```bash
# Get all users
curl http://localhost:8080/api/users

# Create a user
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","address":"123 Main St"}'

# Get user by ID
curl http://localhost:8080/api/users/1

# Update a user
curl -X PUT http://localhost:8080/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Smith","email":"johnsmith@example.com","address":"456 Oak Ave"}'

# Delete a user
curl -X DELETE http://localhost:8080/api/users/1
```

## Native Build

This application uses GraalVM for native compilation, providing:

- **Faster startup time**: Sub-second startup
- **Lower memory consumption**: Reduced memory footprint
- **Smaller container size**: Minimal runtime image
- **Better performance**: Ahead-of-time compilation

## Security Considerations

- Input validation on all endpoints
- SQL injection protection via JPA
- Connection pooling with HikariCP
- Health check endpoints secured by default

## Production Deployment

For production deployment:

1. Use environment variables for database credentials
2. Configure proper logging
3. Set up monitoring and alerting
4. Implement backup strategies for PostgreSQL
5. Use HTTPS with reverse proxy

## Project Status

- ✅ CRUD operations fully implemented
- ✅ PostgreSQL integration
- ✅ Docker containerization
- ✅ Health checks
- ✅ Native image build
- ✅ Comprehensive testing
- ✅ Production ready

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request