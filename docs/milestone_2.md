# MotoTrack — Milestone 2 Progress

## Overview

MotoTrack is a full-stack web application designed to help motorcycle owners track maintenance history, monitor service intervals (based on mileage and time), and stay up to date with upcoming services.

Since Milestone 1, our team has successfully moved from planning and design into implementation. This milestone demonstrates a working MVP (Minimum Viable Product) that includes core functionality across the front-end, back-end, and database layers.

The application now supports real user workflows and persistent data storage, meeting the foundational requirements of the capstone project.

---

## Current Functionality

The following features are fully implemented and working:

### 1. User Authentication
- Users can register a new account
- Users can log in using their credentials
- JWT authentication is used to secure API endpoints

### 2. Motorcycle Management
- Users can create motorcycle profiles
- Each motorcycle is tied to the authenticated user
- Users can view their motorcycles

### 3. Maintenance Logging
- Users can create maintenance logs (e.g., oil changes, tire replacements)
- Logs are stored in the database and linked to a specific motorcycle
- Users can view maintenance history

### 4. Dashboard
- Displays recent maintenance activity
- Shows services that are due based on mileage or time intervals
- Aggregates user-specific data into a simple overview

### 5. Data Persistence
- All data is stored in a relational database (SQLite)
- Relationships exist between users, motorcycles, and maintenance logs

---

## System Demonstration

The application has been tested through real usage scenarios:

### Core Workflow Demonstrated
1. User registers a new account
2. User logs into the system
3. User creates a motorcycle profile
4. User logs a maintenance event
5. User views the dashboard and maintenance history

This confirms that the full stack (front-end, API, database) is functioning correctly.

---

## Screenshots / Demo Evidence

The following should be included in the GitHub repository:

- Screenshot of login/registration page
- Screenshot of motorcycle creation form
- Screenshot of maintenance log creation
- Screenshot of dashboard displaying data

(Alternatively, a video demonstration showing the workflow in real time is included.)

---

## Technical Progress

### Backend
- REST API implemented using Flask
- JWT-based authentication system
- CRUD operations for motorcycles and maintenance logs
- Business logic for service interval tracking

### Frontend
- Basic UI implemented using HTML, CSS, and JavaScript
- Forms for user input and interaction
- Dynamic data rendering from API responses

### Database
- SQLite database configured and connected
- Tables:
  - Users
  - Motorcycles
  - Maintenance Logs
- Proper relationships enforced between entities

---

## Challenges Encountered

- Structuring the project correctly for a full-stack application
- Ensuring authentication works across all protected routes
- Managing relationships between users, motorcycles, and logs
- Organizing the repository to follow best practices

These challenges were resolved through iterative testing, debugging, and restructuring.

---

## Next Steps

The following features are planned for future development:

- Edit and update functionality for motorcycles and maintenance logs
- Email/SMS reminder integration for upcoming services
- Improved dashboard UI and user experience
- Input validation and error handling improvements
- Automated testing (unit and integration tests)

---

## Conclusion

Milestone 2 represents a successful transition from design to implementation. The MotoTrack application now includes a working full-stack system with core features and persistent data.