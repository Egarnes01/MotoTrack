# MotoTrack – Requirements Analysis

## 1. Problem Identification

Motorcycle owners often struggle to consistently track routine maintenance such as oil changes, chain adjustments, brake servicing, and tire replacements. Unlike many modern automobiles, motorcycles typically lack integrated service reminder systems. Riders frequently rely on memory, handwritten notes, or scattered digital reminders, which can lead to missed maintenance, safety risks, reduced vehicle performance, and increased long-term repair costs.

MotoTrack aims to solve this problem by providing a centralized, digital maintenance tracking system tailored specifically to motorcycle owners.

---

## 2. Stakeholders

- Motorcycle owners (primary users)
- Capstone project team members
- Course instructor (project evaluator)
- Potential future users providing feedback during testing

---

## 3. Functional Requirements

The system shall:

1. Allow users to create and manage secure accounts.
2. Allow users to create one or more motorcycle profiles.
3. Store motorcycle details including make, model, year, and current mileage.
4. Allow users to log maintenance activities (e.g., oil change, chain service).
5. Store maintenance history persistently in a database.
6. Automatically calculate service intervals based on mileage or date.
7. Display upcoming and overdue maintenance tasks.
8. Allow users to update motorcycle mileage.
9. Allow users to edit or delete maintenance records.
10. Provide a dashboard view summarizing maintenance status.

---

## 4. Non-Functional Requirements

### Performance
- The system should load pages within a reasonable time under normal usage.
- Maintenance calculations should execute without noticeable delay.

### Security
- User authentication must be required to access personal data.
- Passwords must be securely stored using hashing.
- Users may only access their own data.

### Usability
- The interface should be simple and intuitive for non-technical users.
- Navigation should be consistent across all pages.

### Reliability
- User data must persist across sessions.
- The system should handle invalid inputs gracefully.

### Maintainability
- Code should follow standard naming conventions and documentation practices.
- The system architecture should allow for future feature expansion.

---

## 5. Scope Definition

### In Scope
- Web-based application
- User authentication
- Motorcycle profiles
- Maintenance logging
- Automated service reminders
- Database-backed persistence

### Out of Scope
- Native mobile application
- Dealer or manufacturer integrations
- Advanced analytics or AI-based diagnostics
- Push notifications (email reminders may be considered optional)

---

## 6. Constraints

- Project must be completed within a single academic semester.
- Development limited to technologies approved by the course.
- Team size limited to current group members.
- Hosting and deployment may be limited to local or academic environments.

---

## 7. Assumptions

- Users have internet access and a modern web browser.
- Users will manually input mileage and maintenance data.
- The application will initially support a single language (English).

---

## 8. Success Criteria

The project will be considered successful if:
- All functional requirements are implemented and demonstrable.
- Data is reliably stored and retrieved from the database.
- Multiple user workflows are supported without errors.
- The system passes basic user testing with positive feedback.
- The application meets capstone technical and documentation requirements.
