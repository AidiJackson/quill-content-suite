# Quillography Content Suite - Development Workflow

This document outlines the recommended development workflow for building features across the entire Quillography Content Suite ecosystem.

---

## Overview

The Quillography Content Suite development follows a structured workflow from GitHub issues through implementation, testing, design, and deployment.

### Development Stages
1. **Planning** (GitHub Issues)
2. **Backend Development** (Claude Code)
3. **Testing & Validation** (Replit/Local)
4. **UI/UX Design** (Figma)
5. **Frontend Development** (Replit/VSCode)
6. **Integration & Deployment**

---

## Workflow Diagram

```
┌─────────────┐
│   GitHub    │  Issue Creation & Planning
│   Issues    │  Feature specifications
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Claude    │  Backend Implementation
│    Code     │  API endpoints, services, models
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Replit    │  Testing & Validation
│             │  API testing, integration tests
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Figma     │  UI/UX Design
│             │  Screens, components, prototypes
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Frontend   │  React/Next.js Implementation
│   Replit    │  Component development
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Production │  Deploy & Monitor
│  Deployment │  CI/CD, monitoring
└─────────────┘
```

---

## Stage 1: Planning (GitHub Issues)

### Creating Issues

**Template for Feature Requests:**
```markdown
### Feature Description
[Clear description of the feature]

### User Story
As a [user type], I want [goal] so that [benefit].

### Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Technical Considerations
- Backend changes needed
- Frontend changes needed
- Database migrations required
- External services/APIs

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Priority
[High / Medium / Low]

### Labels
`feature`, `backend`, `frontend`, `design`
```

**Template for Bug Reports:**
```markdown
### Bug Description
[What's wrong]

### Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Environment
- Browser/OS:
- Version:
- Deployment:

### Screenshots/Logs
[If applicable]

### Labels
`bug`, `priority-high`
```

---

## Stage 2: Backend Development (Claude Code)

### Setup

```bash
# Clone repository
git clone https://github.com/your-org/quill-content-suite.git
cd quill-content-suite

# Create feature branch
git checkout -b feature/new-feature-name

# Install dependencies
make install

# Run migrations
make migrate
```

### Development Process

1. **Implement Models** (if needed)
   ```python
   # app/models/new_model.py
   class NewModel(Base, UUIDMixin, TimestampMixin):
       __tablename__ = "new_models"
       # fields...
   ```

2. **Create Schemas**
   ```python
   # app/schemas/new_model.py
   class NewModelCreate(BaseModel):
       # fields...

   class NewModelResponse(BaseModel):
       # fields...
   ```

3. **Implement Service**
   ```python
   # app/services/new_service.py
   class NewService:
       def __init__(self, db: Session):
           self.db = db

       def create(self, data):
           # implementation
   ```

4. **Create Routes**
   ```python
   # app/api/routes/new_route.py
   router = APIRouter(prefix="/new", tags=["New Feature"])

   @router.post("/")
   def create_item(data: NewModelCreate, db: DBSession):
       # implementation
   ```

5. **Write Tests**
   ```python
   # tests/test_new_feature.py
   def test_create_item(client, headers):
       response = client.post("/new", json={...}, headers=headers)
       assert response.status_code == 201
   ```

6. **Run Tests**
   ```bash
   make test
   ```

7. **Format Code**
   ```bash
   make format
   ```

### Migration Workflow

```bash
# Create migration
make makemigration
# Enter description: "Add new_model table"

# Review migration
cat alembic/versions/xxx_add_new_model_table.py

# Apply migration
make migrate
```

### Commit Guidelines

```bash
# Feature commits
git commit -m "feat: add new content type endpoint"

# Bug fixes
git commit -m "fix: resolve virality scoring edge case"

# Documentation
git commit -m "docs: update API reference for new endpoint"

# Tests
git commit -m "test: add tests for new content type"

# Refactor
git commit -m "refactor: optimize database queries"
```

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Maintenance

---

## Stage 3: Testing & Validation (Replit)

### Replit Setup

1. **Import from GitHub**
   - Connect GitHub account
   - Import `quill-content-suite` repository

2. **Configure Environment**
   ```bash
   # .replit file
   run = "uvicorn app.main:app --host 0.0.0.0 --port 8000"

   [env]
   DATABASE_URL = "sqlite:///./quillography.db"
   USE_FAKE_AI = "true"
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start Server**
   ```bash
   make run
   ```

### Testing Checklist

- [ ] Health check responds
- [ ] New endpoints return correct status codes
- [ ] Request validation works
- [ ] Response format matches schema
- [ ] Database operations succeed
- [ ] Error handling works correctly
- [ ] All tests pass

### API Testing with Swagger

1. Navigate to `https://your-repl.repl.co/docs`
2. Test each new endpoint
3. Verify request/response formats
4. Check error cases

### Manual Testing with cURL

```bash
# Test new endpoint
curl -X POST https://your-repl.repl.co/api/endpoint \
  -H "Content-Type: application/json" \
  -H "X-User-Id: test-user" \
  -d '{"field": "value"}'
```

---

## Stage 4: UI/UX Design (Figma)

### Figma Workflow

1. **Create Feature Frame**
   - Name: `[Feature Name] - [View]`
   - Example: `Blog Generator - Input Form`

2. **Design Screens**
   - Desktop view (1440px)
   - Tablet view (768px)
   - Mobile view (375px)

3. **Use Component Library**
   - Reference `UI_BRIEF_FIGMA.md`
   - Use existing components
   - Maintain design system consistency

4. **Create Prototype**
   - Link screens with interactions
   - Add hover states
   - Include loading states
   - Show error states

5. **Annotate Designs**
   - API endpoints used
   - Data requirements
   - Interaction notes
   - Edge cases

### Design Review Checklist

- [ ] Follows design system
- [ ] Responsive across breakpoints
- [ ] Accessibility considerations
- [ ] Loading states included
- [ ] Error states included
- [ ] Empty states included
- [ ] Interactive prototype complete

---

## Stage 5: Frontend Development

### Frontend Setup (React/Next.js)

```bash
# Create Next.js app
npx create-next-app@latest quillography-frontend --typescript --tailwind

cd quillography-frontend

# Install dependencies
npm install @tanstack/react-query axios zod react-hook-form
```

### Project Structure

```
quillography-frontend/
├── app/
│   ├── (dashboard)/
│   │   ├── page.tsx
│   │   └── layout.tsx
│   ├── projects/
│   │   └── [id]/
│   │       └── page.tsx
│   └── create/
│       └── page.tsx
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   └── features/
│       ├── ContentGenerator.tsx
│       └── ViralityScore.tsx
├── lib/
│   ├── api.ts
│   └── utils.ts
└── types/
    └── index.ts
```

### API Integration

```typescript
// lib/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'X-User-Id': 'user-123', // Replace with auth
  },
});

export const generateBlog = async (data: BlogRequest) => {
  const response = await api.post('/content/blog', data);
  return response.data;
};
```

### Component Development

```typescript
// components/features/ContentGenerator.tsx
'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { generateBlog } from '@/lib/api';

export function ContentGenerator() {
  const [topic, setTopic] = useState('');

  const mutation = useMutation({
    mutationFn: generateBlog,
    onSuccess: (data) => {
      console.log('Generated:', data);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate({ topic });
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
    </form>
  );
}
```

### Testing Frontend

```bash
# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

---

## Stage 6: Integration & Deployment

### Pre-Deployment Checklist

**Backend:**
- [ ] All tests passing
- [ ] Code formatted and linted
- [ ] Migrations ready
- [ ] Environment variables documented
- [ ] API documentation updated

**Frontend:**
- [ ] All features working
- [ ] Responsive design verified
- [ ] Cross-browser tested
- [ ] Performance optimized
- [ ] Error boundaries added

### Deployment Process

#### Backend Deployment

```bash
# Production environment setup
export ENVIRONMENT=production
export DATABASE_URL=postgresql://...
export USE_FAKE_AI=false
export OPENAI_API_KEY=sk-...

# Run migrations
alembic upgrade head

# Start production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Configure environment variables in Vercel dashboard
NEXT_PUBLIC_API_URL=https://api.quillography.com
```

### Post-Deployment

1. **Smoke Testing**
   - Health check responds
   - Critical paths work
   - Database connection healthy

2. **Monitoring**
   - Check error logs
   - Monitor response times
   - Track API usage

3. **Documentation**
   - Update API_REFERENCE.md
   - Update README.md
   - Create release notes

---

## Pull Request Workflow

### Creating PR

```markdown
### Description
[What does this PR do]

### Related Issue
Closes #123

### Changes Made
- Added new feature X
- Fixed bug Y
- Updated documentation Z

### Testing
- [ ] All tests pass
- [ ] Manual testing complete
- [ ] API documentation updated

### Screenshots
[If UI changes]

### Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**
   - Tests must pass
   - Linting must pass
   - No merge conflicts

2. **Code Review**
   - At least 1 approval required
   - Address all comments
   - Ensure best practices

3. **Merge**
   - Squash and merge for clean history
   - Delete branch after merge

---

## Continuous Improvement

### Retrospective Questions

After each major feature:
1. What went well?
2. What could be improved?
3. What should we start doing?
4. What should we stop doing?

### Metrics to Track

- Development velocity
- Bug count
- Test coverage
- API response times
- User feedback

---

## Tools & Resources

### Required Tools
- **Git**: Version control
- **GitHub**: Issue tracking, PRs
- **Claude Code**: Backend development
- **Replit**: Testing environment
- **Figma**: UI/UX design
- **VSCode**: Alternative IDE

### Recommended Extensions
- **VSCode**: Python, Pylance, Black Formatter
- **Browser**: React DevTools, JSON Viewer

### Documentation Links
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [React Query Docs](https://tanstack.com/query/latest)
- [Next.js Docs](https://nextjs.org/docs)

---

## Contact & Support

### For Questions
- **GitHub Issues**: Technical problems
- **GitHub Discussions**: General questions
- **Slack/Discord**: Team communication

### Review Schedule
- **Daily**: Standup (async)
- **Weekly**: Sprint planning
- **Bi-weekly**: Sprint retrospective

---

Last Updated: 2024
Version: 1.0
