# MotoTrack — Testing Plan

MotoTrack is a full-stack web application designed to help motorcycle owners track maintenance history, monitor service intervals (mileage and time-based), and receive reminders for upcoming services.

This document outlines the structured testing strategy that will be used to ensure correctness, security, reliability, and maintainability before deployment.

---

# 1. Testing Strategy Overview

## Testing Philosophy

MotoTrack will use a layered testing approach:

- Unit Testing — Validate business logic in isolation (interval calculations, validation, ownership checks).
- Integration Testing — Validate communication between API, database, and authentication layers.
- System / End-to-End Testing — Validate complete user workflows.
- Non-Functional Testing Considerations — Address performance, security, and input validation risks.

The goal is to catch defects early, prevent regressions, and protect critical logic such as service interval calculations and authentication.

---

## Testing Types and Why

### Unit Testing

Used for:
- Interval calculations
- Validation logic
- Authorization helpers
- Dashboard aggregation logic

Reason:
Fast, isolated, and prevents core logic errors.

---

### Integration Testing

Used for:
- API endpoints interacting with database
- Authentication (JWT)
- Ownership enforcement
- Maintenance log creation and dashboard updates

Reason:
Ensures layers work correctly together.

---

### System / End-to-End Testing

Used for:
- Full user workflows
- Realistic usage scenarios

Reason:
Validates the system from a user perspective.

---

## Tools

- pytest
- pytest-django
- Django test database (SQLite for development)
- pytest-cov (coverage reporting)
- unittest.mock or pytest-mock (for external reminder services)

---

## Testing in the Sprint Process

- Every user story must include corresponding tests.
- Tests must pass before pull requests are merged.
- CI (GitHub Actions) will run automated tests on every PR.
- Code is not considered “Done” unless tests are included.

---

## Responsibility

- Developers test the features they build.
- A rotating sprint reviewer verifies:
  - Tests exist
  - Edge cases are included
  - CI passes

---

# 2. Unit Test Plan

Below are critical units requiring unit testing.

---

## Unit 1 — calculate_next_due_mileage

Function Purpose:
Calculates the next service mileage based on current mileage and interval.

Test Cases:

- Input: current_mileage=12000, interval_miles=3000  
  Expected Output: 15000

- Input: current_mileage=14999, interval_miles=3000  
  Expected Output: 17999

Edge Case:

- Input: interval_miles=0  
  Expected: Raise ValueError

---

## Unit 2 — calculate_next_due_date

Function Purpose:
Calculates next service due date using day interval.

Test Cases:

- Input: 2026-01-01, interval_days=30  
  Expected Output: 2026-01-31

- Input: 2026-02-15, interval_days=180  
  Expected Output: Correct date 180 days later

Edge Case:

- Input: last_service_date=None  
  Expected: Raise ValueError

---

## Unit 3 — user_owns_motorcycle

Function Purpose:
Ensures users can only access their own motorcycles.

Test Cases:

- Input: user_id=5, motorcycle_user_id=5  
  Expected Output: True

- Input: user_id=5, motorcycle_user_id=9  
  Expected Output: False

Edge Case:

- Input: user_id=None  
  Expected Output: False

---

## Unit 4 — validate_maintenance_log

Function Purpose:
Validates service type, mileage, and date fields.

Test Cases:

- Input: valid service type, mileage 5000  
  Expected: Pass validation

- Input: valid service type, mileage 8000  
  Expected: Pass validation

Edge Case:

- Input: mileage -1  
  Expected: Raise ValidationError

---

## Unit 5 — build_dashboard_summary

Function Purpose:
Builds dashboard response including recent logs and upcoming services.

Test Cases:

- Motorcycle has 3 logs  
  Expected: recent_logs length = 3

- Motorcycle has 0 logs  
  Expected: recent_logs empty but no crash

Edge Case:

- Invalid motorcycle ID  
  Expected: Raise NotFound or return 404 equivalent

---

## Example pytest Snippet

```python
import pytest
from mototrack.services.intervals import calculate_next_due_mileage

def test_next_due_mileage_normal():
    assert calculate_next_due_mileage(12000, 3000) == 15000

def test_next_due_mileage_zero_interval():
    with pytest.raises(ValueError):
        calculate_next_due_mileage(12000, 0)
```

---

# 3. Integration Test Plan

## Integration 1 — Authentication Flow

Components Tested:
- Registration endpoint
- Login endpoint
- JWT issuance
- Protected route access

Validated:
- Valid token allows access
- Invalid or missing token blocks access

Expected Result:
- Valid token → 200 OK
- Invalid token → 401 Unauthorized

Failure Scenario:
- Wrong password → login fails

---

## Integration 2 — Motorcycle CRUD (API ↔ Database)

Components Tested:
- API endpoints
- Django ORM
- Database persistence

Validated:
- Create, read, update, delete operations
- Ownership enforcement

Expected Result:
- Owner can access motorcycle
- Non-owner receives 403 or 404

Failure Scenario:
- Unauthorized delete attempt is blocked

---

## Integration 3 — Maintenance Log + Dashboard Update

Components Tested:
- Log creation endpoint
- Database write
- Dashboard query logic

Validated:
- Log stored correctly
- Dashboard reflects new entry

Expected Result:
- 201 Created
- Dashboard shows new log

Failure Scenario:
- Missing required field → 400 Bad Request

---

## Integration 4 — Reminder Service (Mocked)

Components Tested:
- Reminder scheduling logic
- Notification client wrapper

Validated:
- Correct message payload formed
- Send method invoked once

Failure Scenario:
- External service failure handled without crashing app

---

# 4. System / End-to-End Test Scenarios

## Scenario A — New User Full Workflow

Steps:
1. Register account
2. Login
3. Create motorcycle
4. Add maintenance log
5. View dashboard

Expected Outcome:
- All operations succeed
- Maintenance appears in history
- Upcoming service calculated correctly

Possible Failure Points:
- Duplicate registration
- Missing token
- Invalid mileage input
- Ownership access violation

---

## Scenario B — Mileage Update Triggers Service Alert

Steps:
1. Login
2. Update motorcycle mileage
3. Open dashboard
4. Confirm service shows as due soon

Expected Outcome:
- Mileage persists
- Interval recalculates correctly
- Dashboard updates accordingly

Possible Failure Points:
- Validation error
- Dashboard calculation error
- Off-by-one interval bug

---

# 5. Non-Functional Testing Considerations

## Performance

- Dashboard queries must scale as logs increase.
- Avoid N+1 query issues.
- Use pagination for maintenance history.

## Security

- All protected routes require JWT.
- Prevent IDOR (Insecure Direct Object Reference).
- Ensure no sensitive user data leaks in responses.

## Input Validation

- Mileage must be non-negative.
- Required fields must be enforced.
- Service types must match allowed values.

## Error Handling

- Consistent JSON error responses.
- External notification failures must not crash the server.
- Proper HTTP status codes returned.

---

# 6. Defect Tracking Method

## How Bugs Are Tracked

GitHub Issues will be used for defect tracking.

Each bug must include:
- Steps to reproduce
- Expected result
- Actual result
- Environment details

## Labels Used

- bug
- security
- backend
- frontend
- testing
- high-priority

## Resolution Process

- Developer assigned to issue
- Fix submitted via pull request
- Tests added or updated
- CI must pass
- Sprint reviewer verifies before closing issue
