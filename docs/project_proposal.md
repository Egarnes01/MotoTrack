# MotoTrack: Motorcycle Maintenance & Service Log

## 1. Project Overview

MotoTrack is a full-stack web application designed to help motorcycle owners track maintenance, service intervals, and vehicle history in a centralized, easy-to-use platform. Many riders rely on memory, paper notes, or scattered phone reminders, which often leads to missed maintenance, reduced performance, safety risks, and unnecessary repair costs.

MotoTrack solves this problem by providing riders with structured maintenance logs, automated service reminders, and motorcycle-specific profiles that persist over time.

---

## 2. Problem Definition & Objectives

### Problem Statement
Motorcycle owners frequently struggle to consistently track essential maintenance tasks such as oil changes, chain adjustments, brake servicing, and tire replacements. Unlike modern cars, motorcycles often lack built-in service tracking systems, and many riders do not want complex dealership software or spreadsheets.

This lack of a lightweight, centralized solution can result in:
- Missed or delayed maintenance
- Increased safety risks
- Reduced motorcycle lifespan
- Lower resale value

### Project Objectives
The primary objectives of MotoTrack are to:
- Provide a centralized digital maintenance log for motorcycle owners
- Track service intervals based on mileage and/or time
- Send reminders for upcoming or overdue maintenance
- Maintain historical service data for long-term ownership and resale value
- Offer a simple and intuitive user experience for everyday riders

Success will be measured by the system’s ability to accurately store data, calculate service intervals, and support multiple user workflows without data loss.

---

## 3. Scope & Feasibility

### In-Scope Features
- User authentication and account management
- Motorcycle profile creation (make, model, year, mileage)
- Maintenance log entries (oil changes, chain service, tires, brakes, inspections)
- Automatic service interval tracking (mileage- or date-based)
- Dashboard view of upcoming and overdue maintenance
- Persistent data storage using a database

### Out-of-Scope Features (for this semester)
- Mobile app deployment (web-only for now)
- Dealership integrations
- Advanced analytics or AI-based recommendations

### Feasibility
The scope is intentionally limited to ensure the project can be completed within a single semester. Core features focus on functionality rather than excessive complexity, while still demonstrating full-stack development, business logic, and database usage. The project builds directly on skills learned in CS coursework and prior projects.

---

## 4. Technology Stack Selection

### Front-End
- **HTML, CSS, JavaScript**
- Optional front-end framework (e.g., Bootstrap) for responsive UI

### Back-End
- **Python with Django**
- REST-style views or service layers to handle business logic

### Database
- **SQLite (development)**  
- Designed to be easily migrated to PostgreSQL if needed

### Version Control
- **GitHub** for source control, collaboration, and documentation

### Justification
Django provides a structured MVC-style architecture, built-in authentication, ORM-based database access, and scalability suitable for a semester-long capstone project. The stack supports rapid development while still allowing room for meaningful business logic and testing.

---

## 5. System Architecture (High-Level)

MotoTrack will follow a **client-server / MVC architecture**:

- **Client (Front-End):**
  - User interface for data entry and viewing maintenance status
- **Server (Back-End):**
  - Handles authentication, maintenance logic, service interval calculations
- **Database Layer:**
  - Stores users, motorcycles, maintenance records, and service schedules

Architecture diagrams will be created and documented in later milestones.

---

## 6. Team Roles & Responsibilities

### Team Members
- **Elijah Garnes**
  - Back-end development
  - Database schema design
  - Business logic implementation
  - Project coordination

- **Levi Green**
  - Front-end development
  - UI/UX design
  - User workflows and usability testing
  - Documentation support

Both members will contribute to planning, testing, and documentation.

---

## 7. Project Plan & Timeline

### Milestone Breakdown

**Milestone 1 – Project Proposal & Planning**
- Finalize project scope and requirements
- Define technology stack and roles
- Submit proposal documentation

**Milestone 2 – Core Implementation**
- Set up project repository and Django environment
- Implement authentication and database models
- Build core maintenance logging features
- Initial UI implementation

**Milestone 3 – Testing, Refinement & Presentation**
- User testing and feedback incorporation
- Bug fixes and performance improvements
- Documentation completion
- Final presentation and demo

### Development Methodology
The team will follow an **iterative Agile-style process**, with features developed in small increments and reviewed regularly through GitHub commits and testing.

---

## 8. Risks & Mitigation

- **Scope Creep:** Controlled by clearly defining out-of-scope features
- **Time Constraints:** Mitigated by prioritizing core functionality early
- **Technical Issues:** Reduced by using familiar frameworks and tools

---

## 9. Conclusion

MotoTrack is a realistic, well-scoped capstone project that addresses a real-world problem faced by everyday motorcycle riders. It meets all functional, technical, architectural, and collaboration requirements while remaining feasible within a single semester. The project demonstrates full-stack development, database integration, and professional project planning.

