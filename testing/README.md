# Testing & Quality Assurance

**QA Lead:** Rishi Nalam

## í¾¯ Overview

This directory contains all testing infrastructure, documentation, and deployment configurations for Rehabit.

## í³ Structure
```
testing/
â”œâ”€â”€ backend_tests/       # Backend API tests
â”œâ”€â”€ frontend_tests/      # Frontend UI tests
â”œâ”€â”€ integration_tests/   # End-to-end tests
â”œâ”€â”€ deployment/         # Deployment scripts
â”œâ”€â”€ docs/              # Documentation
â””â”€â”€ screenshots/       # App screenshots
```

## í·ª Testing Strategy

### 1. Backend Testing
- API endpoint testing
- Database operations testing
- ML model integration testing
- Error handling validation

### 2. Frontend Testing
- UI/UX manual testing
- Responsive design testing
- Cross-browser compatibility
- User flow validation

### 3. Integration Testing
- Frontend-Backend communication
- Complete user journeys
- Data consistency checks

## íº€ Quick Start

### Run Backend Tests
```bash
cd backend
pytest ../testing/backend_tests/ -v
```

### Manual Frontend Tests
See `frontend_tests/manual_test_checklist.md`

### Integration Tests
See `integration_tests/end_to_end_tests.md`

## í³Š Test Coverage Goals

- Backend API: 80%+ endpoint coverage
- Frontend: All critical user flows
- Integration: Complete happy path + error scenarios

## í°› Bug Tracking

Bugs are tracked in GitHub Issues with labels:
- `bug` - Something isn't working
- `critical` - Blocks demo/presentation
- `enhancement` - Nice to have

## í³ˆ Quality Metrics

- All API endpoints return 200/201 for valid requests
- Page load time < 3 seconds
- No console errors in production
- Mobile responsive (375px to 1920px)

---

**Last Updated:** Day 1 of Hackathon
