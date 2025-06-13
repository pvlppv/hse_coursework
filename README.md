# System for tracking personal data built as a modern web-application

## Tech Stack

### Frontend

- Vue.js 3 with Composition API
- Vite as build tool
- TailwindCSS for styling
- AG Grid for data tables
- ECharts for data visualization
- Vue Router for navigation
- PWA support

### Backend

- FastAPI (Python)
- PostgreSQL database
- Redis for caching
- Alembic for database migrations
- SQLAlchemy ORM

### Infrastructure

- Docker and Docker Compose
- Nginx as reverse proxy

## Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.8+ (for local backend development)

## Setup Instructions

### Using Docker (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd pvlppv_web
```

2. Create necessary environment files:

   - Create `backend/.env` file with required environment variables
   - Configure your database credentials and other settings

3. Start the application:

```bash
docker-compose up -d
```

The application will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5433
