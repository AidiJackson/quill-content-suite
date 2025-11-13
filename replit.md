# Quillography Content Suite - Replit Configuration

## Project Overview

**Quillography Content Suite** is a full-stack application featuring an AI-powered FastAPI backend and a modern React frontend for content creation, editing, campaign management, and media processing.

### Key Features
- **Frontend**: Modern React + Vite UI with shadcn/ui components
- **Written Content Generation**: Blogs, newsletters, social posts, campaigns
- **Virality Engine**: Content scoring and optimization
- **Video & Audio Processing**: Trimming, resizing, captions, pitch/tempo shifting
- **Project Management**: Organize content and media with versioning
- **Interactive API Documentation**: Available at `/docs`

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11
- **ORM**: SQLAlchemy 2.x
- **Database**: PostgreSQL (Replit) / SQLite (fallback)
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18 + Vite 6
- **UI Library**: shadcn/ui + Radix UI
- **Styling**: Tailwind CSS
- **Components**: Lucide icons, Recharts
- **Language**: TypeScript

## Replit Setup

### Architecture

The application runs as two separate services:

- **Frontend** (React + Vite): Port 5000 - Exposed via Replit webview
- **Backend** (FastAPI): Port 8000 - Internal API server

Both services start automatically and communicate over localhost.

### Environment Configuration

Default configuration values that work out of the box:

- **Frontend Port**: 5000 (Replit's exposed webview port)
- **Backend Port**: 8000 (internal API server)
- **Backend Host**: 0.0.0.0 (required for Replit)
- **Database**: PostgreSQL (Replit managed) with SQLite fallback
- **CORS**: Configured to allow frontend requests
- **AI Service**: Uses fake/deterministic AI client by default (no API key needed)

### Optional Environment Variables

If you need to customize settings, you can set these environment variables in Replit Secrets:

- `OPENAI_API_KEY` - Your OpenAI API key (if using real AI instead of fake client)
- `USE_FAKE_AI` - Set to `false` to use real OpenAI client (default: `true`)
- `DATABASE_URL` - Custom database URL (default: `sqlite:///./quillography.db`)
- `ENVIRONMENT` - Environment name (default: `development`)
- `DEBUG` - Enable debug mode (default: `true`)
- `LOG_LEVEL` - Logging level (default: `INFO`)

### Running the Application

#### Development Mode

Both frontend and backend run as separate services:

**Frontend (React + Vite)** - Port 5000:
```bash
cd frontend && npm run dev -- --host 0.0.0.0 --port 5000
```
- Served via Replit webview
- Proxies `/api` requests to backend at `localhost:8000`

**Backend (FastAPI)** - Port 8000:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Internal API server
- All routes prefixed with `/api`

#### Production Mode (Autoscale Deployment)

Single FastAPI server on port 5000 serves both:
- Static React build from `frontend/build/`
- API endpoints at `/api/*`

The deployment automatically:
1. Builds frontend: `cd frontend && npm run build`
2. Starts backend: `uvicorn app.main:app --host 0.0.0.0 --port 5000`

### Accessing the Application

**Development**:
- **Frontend UI**: Via Replit webview (port 5000)
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Health Check**: `http://localhost:8000/api/health`

**Production**:
- **Everything**: Via your published Replit domain (port 5000)
- **API Documentation**: `https://your-domain/docs` (Swagger UI)
- **Health Check**: `https://your-domain/api/health`

### Project Structure

```
quill-content-suite/
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── components/    # UI components (shadcn/ui)
│   │   ├── styles/        # Global styles
│   │   ├── App.tsx        # Main app component
│   │   └── main.tsx       # Entry point
│   ├── package.json       # Frontend dependencies
│   ├── vite.config.ts     # Vite configuration
│   └── .env               # Frontend environment vars
├── app/                   # FastAPI backend
│   ├── api/
│   │   ├── routes/        # API endpoints
│   │   └── deps.py        # Dependencies (auth, DB)
│   ├── core/              # Configuration and logging
│   ├── db/                # Database setup
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── utils/             # Utilities
│   └── main.py            # FastAPI app
├── alembic/               # Database migrations
├── tests/                 # Backend test suite
├── requirements.txt       # Python dependencies
└── Makefile              # Development commands
```

## API Endpoints

### Content Generation
- `POST /content/blog` - Generate blog posts
- `POST /content/newsletter` - Generate newsletters
- `POST /content/post` - Generate social media posts
- `POST /content/campaign` - Generate campaigns

### Virality Engine
- `POST /virality/score` - Score content virality
- `POST /virality/optimize` - Optimize content for engagement
- `POST /virality/rewrite` - Rewrite content for better virality

### Media Processing
- `POST /video/trim` - Trim videos
- `POST /video/resize` - Resize videos
- `POST /audio/pitch` - Shift audio pitch
- `POST /audio/tempo` - Adjust audio tempo

### Project Management
- `GET /projects` - List projects
- `POST /projects` - Create project
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

### System
- `GET /health` - Health check endpoint
- `GET /` - Welcome message with API info

## Development

### Database Migrations

The application creates database tables on startup via `init_db()` in `app/main.py`. The initial migration has already been applied.

To create and apply new migrations manually:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

**Note**: For production deployments, you should run `alembic upgrade head` before starting the server to ensure the database schema is up to date.

### Running Tests

```bash
pytest -v
```

### Code Quality

```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint code
ruff check app/ tests/
```

## Deployment

The application is configured for **autoscale deployment** on Replit in the `.replit` file:

```toml
[deployment]
deploymentTarget = "autoscale"
run = ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

When you publish this Repl:
- The server will automatically scale based on traffic
- The API will be accessible via your custom Replit domain
- Interactive documentation will be available at `/docs`

### Production Considerations

For production deployments:
1. **Database**: Consider using PostgreSQL instead of SQLite for production
   - Update `DATABASE_URL` environment variable
   - Run `alembic upgrade head` to apply migrations before first start
2. **API Keys**: Set proper environment variables for external services
   - Set `OPENAI_API_KEY` if using real AI client
   - Set `USE_FAKE_AI=false` to enable OpenAI integration
3. **Security**: 
   - Enable API key authentication if needed (`API_KEY_ENABLED=true`)
   - Configure specific CORS origins instead of wildcard `*`
   - Update `CORS_ORIGINS` to only include trusted domains
4. **Environment**: Set `ENVIRONMENT=production` and `DEBUG=false`

## Recent Changes

- **2025-11-13**: Full-stack setup completed
  - Configured Python 3.11 and Node.js 20 environments
  - Extracted and integrated React + Vite frontend with shadcn/ui components
  - Backend moved to port 8000, frontend on port 5000
  - Updated CORS to allow frontend requests
  - Configured dual workflows for frontend and backend
  - Database migrations completed successfully
  - Autoscale deployment configured

## Architecture

### Service Layer Pattern
- **Routes**: Handle HTTP requests and responses
- **Services**: Business logic isolated from routes
- **Models**: Database schema (SQLAlchemy ORM)
- **Schemas**: Request/response validation (Pydantic)
- **Dependencies**: Reusable components via FastAPI DI

### AI Client Architecture
The system uses a pluggable AI client pattern:
- **FakeAIClient**: Deterministic responses for testing (default)
- **OpenAIAIClient**: OpenAI integration (requires API key)

Switch between clients via `USE_FAKE_AI` environment variable.

## Support & Documentation

- API Documentation: `/docs` endpoint (Swagger UI)
- Project README: `README.md`
- API Reference: `API_REFERENCE.md`
- Roadmap: `CONTENT_SUITE_ROADMAP.md`
- UI Brief: `UI_BRIEF_FIGMA.md`

## Notes

- The fake AI client provides deterministic responses, perfect for testing and development
- All API endpoints return JSON responses
- The application uses SQLite by default for easy development
- Database file (`quillography.db`) is created automatically
- All database tables are created on first startup
