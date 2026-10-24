#  Gym Management System

A Python Full Stack Development Project using FastAPI

# Project Overview

The Gym Management System is a RESTful API application developed using FastAPI to manage gym operations efficiently. It provides features for user authentication, membership subscriptions, gym plans, attendance tracking, trainer assignments, and administrative management.

The system follows a modular architecture that separates routers, models, schemas, dependencies, and database operations to improve maintainability, scalability, and code reusability.

# Project Objectives

- Automate gym membership and subscription management.
- Provide secure user authentication and role-based access control.
- Manage gym plans and membership details.
- Track member attendance.
- Allow administrators to manage users and gym operations.
- Support trainer assignments and membership supervision.
- Provide interactive API documentation using Swagger UI.
- Follow Agile methodology and Software Development Life Cycle (SDLC) practices.

# Features

# 1. Authentication Module
- User registration and login.
- Password hashing and verification.
- Token-based authentication.
- Role-based authorization.
- Access control for protected endpoints.

#  2. Plans Module
- Create and manage gym plans.
- Retrieve available plans.
- View plan details.
- Control access to plan management operations based on user roles.

#  3. Membership Module
- Subscribe to gym membership plans.
- Retrieve membership information.
- Associate users with membership plans.
- Track membership status and subscription details.
- Support membership management according to the implemented business rules.

#  4. Attendance Module
- Record gym attendance.
- Retrieve attendance records.
- Associate attendance entries with gym members.
- Support attendance monitoring.

#  5. Admin Module
- Retrieve and manage user information.
- Access administrative operations.
- Assign trainers to members or memberships.
- Enforce administrator-level permissions.

#  6. Trainer Module
- Manage trainer-related information.
- Support trainer assignments.
- Retrieve relevant member or membership information based on authorization rules.

#  Technology Stack

| Technology | Purpose |

| Python | Core programming language |
| FastAPI | REST API development |
| Pydantic | Request validation and response schemas |
| SQLAlchemy | ORM and database operations |
| MySQL / SQLite | Database storage, depending on configuration |
| Uvicorn | ASGI server |
| JWT / OAuth2 | Authentication, if configured |
| Passlib / pwdlib | Password hashing, depending on implementation |
| PyMySQL | MySQL connectivity, if using the MySQL driver |
| Swagger UI | Interactive API testing |
| Git and GitHub | Version control and source-code management |

*The exact libraries and database depend on the packages and configuration used in your implementation.*

#  Project Structure

text
gym-management-system/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── plans.py
│       ├── memberships.py
│       ├── attendance.py
│       ├── admin.py
│       └── trainer.py
│
├── tests/
│   └── test_main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md


Note: Adjust the directory and filenames above to match your actual project. Your routers may use different filenames.

#   Installation and Setup

#  Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible version supported by your dependencies.
- pip package manager.
- MySQL, if configured as your database.
- Git (optional).

#  Step 1: Clone the Repository

bash
git clone https://github.com/pardha2/gym_management
cd gym-management


Replace the placeholder with your actual repository URL.

#  Step 2: Create a Virtual Environment

Windows:

bash
python -m venv venv


Activate it:

bash
venv\Scripts\activate


#  Step 3: Install Dependencies

bash
pip install -r requirements.txt


If you have not created `requirements.txt` yet, install the packages your implementation uses, for example:

bash
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv


Add the appropriate database driver and authentication libraries if required.

#  Step 4: Configure Environment Variables

Create a `.env` file in the project root.

Example for MySQL:

env
DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@localhost:3306/gym_db
SECRET_KEY=replace_with_a_secure_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


Replace the database credentials and secret with your own values. Keep `.env` private and never commit production secrets to GitHub.

If you use SQLite or a different database, update the configuration accordingly.

#  Step 5: Run the Application

If your FastAPI instance is `app` inside `app/main.py`, run:

bash
uvicorn app.main:app --reload


If your `main.py` is in the project root, use:

bash
uvicorn main:app --reload


The server will usually run at:

text
http://127.0.0.1:8000


#  📖 API Documentation

FastAPI automatically generates interactive API documentation.

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| Root endpoint | http://127.0.0.1:8000/ |

Use Swagger UI to inspect endpoints, submit request bodies, test responses, and verify error handling.

#  🔗 API Modules and Endpoints

The following endpoint paths reflect the router prefixes in the project. Individual routes and HTTP methods should be verified against the implementation.

| Module | Example endpoint | Purpose |
|---|---|---|
| Authentication | `/auth/` | Authentication-related operations |
| Plans | `/plans/` | Gym plan operations |
| Memberships | `/memberships/` | Membership subscriptions |
| Attendance | `/attendance/` | Attendance operations |
| Admin | `/admin/users` | Administrative user operations |
| Trainer | `/trainer/` | Trainer-related operations |

#  Example API Requests

Register a user

http
POST /auth/register
Content-Type: application/json


Example request body — adapt the fields to your registration schema:

json
{
  "name": "Rahul",
  "email": "rahul@example.com",
  "password": "ExamplePassword123",
  "role": "member"
}


Log in

http
POST /auth/login
Content-Type: application/x-www-form-urlencoded


If the endpoint uses `OAuth2PasswordRequestForm`, submit form fields such as:

text
username=rahul@example.com
password=ExamplePassword123


Create a gym plan

http
POST /plans/
Content-Type: application/json


Example request body — adjust to the plan schema:

json
{
  "name": "Monthly Plan",
  "duration": 30,
  "price": 1500
}


Subscribe to a membership

http
POST /memberships/
Content-Type: application/json


The request body must follow the membership subscription schema defined by your application.

Record attendance

http
POST /attendance/
Content-Type: application/json


Use the member identifier and attendance fields required by your attendance schema.

*These request bodies are illustrative examples, not guarantees of the exact fields accepted by your endpoints. Check `/docs` for the actual schemas.*

#   Application Workflow

text
                 START
                   |
                   v
          User Registration
                   |
                   v
           User Authentication
                   |
                   v
           Access Token Issued
                   |
                   v
          Role-Based Authorization
                   |
          +--------+---------+
          |        |         |
          v        v         v
        Admin    Member    Trainer
          |        |         |
          v        v         v
      Manage     View /    Trainer
      Users      Subscribe Assignments
          |        |
          |        v
          |    Membership
          |        |
          |        v
          |     Attendance
          +--------+---------+
                   |
                   v
             Database
                   |
                   v
             API Response


The exact workflow depends on the business rules and authorization checks implemented in the project.

#  Application Architecture

The application follows a layered architecture.

1. Client layer: Swagger UI, Postman, or a frontend application sends HTTP requests.
2. Router layer: FastAPI routers receive requests and direct them to the appropriate operations.
3. Validation layer: Pydantic schemas validate incoming data and structure responses.
4. Dependency layer: Shared dependencies provide database sessions and authentication or role checks.
5. Business logic layer: Application rules process plans, subscriptions, attendance, and assignments.
6. Model and database layer: SQLAlchemy models map application entities to database tables.
7. Response layer: FastAPI returns JSON data with the appropriate HTTP status code.

#  Security and Validation

The project can enforce the following security practices, depending on the implemented configuration:

- Password hashing instead of storing plaintext passwords.
- Authentication for protected endpoints.
- Role-based access for administrative and trainer operations.
- Pydantic validation of request fields.
- Appropriate HTTP exceptions for invalid requests and unauthorized access.
- Environment variables for database credentials and secret keys.
- Validation of membership and attendance operations against business rules.

#   Testing

Test the API using Swagger UI or Postman.

Recommended test scenarios:

| Scenario | Expected result |
|---|---|
| Register with valid data | User created successfully |
| Register with an existing email | Conflict response, if duplicate emails are prohibited |
| Login with valid credentials | Authentication succeeds |
| Login with invalid credentials | Authentication fails |
| Access a protected route without a token | Unauthorized response |
| Access an admin route as a member | Forbidden response, if role checks are configured |
| Subscribe using a valid plan | Subscription created according to business rules |
| Submit invalid request data | Validation error |
| Retrieve existing attendance | Attendance information returned |

Automated tests can be implemented with `pytest` and FastAPI's `TestClient`.

#   Software Development Life Cycle (SDLC)

The project can be documented using the following SDLC stages:

1. Requirement Analysis: Identify member, trainer, administrator, plan, subscription, and attendance requirements.
2. Planning: Define scope, features, modules, responsibilities, and milestones.
3. System Design: Design the API architecture, database tables, relationships, and request/response schemas.
4. Implementation: Develop FastAPI routers, models, schemas, dependencies, and business rules.
5. Testing: Verify endpoints, input validation, authorization, database operations, and error handling.
6. Deployment: Configure environment variables and deploy to a compatible hosting platform.
7. Maintenance: Fix defects, improve performance, and extend features based on feedback.

#   Agile Methodology

Development can be organized into short iterations or sprints.

| Sprint | Main deliverables |
|---|---|
| Sprint 1 | Requirements, project setup, database configuration |
| Sprint 2 | User registration, login, and authentication |
| Sprint 3 | Gym plans and membership subscriptions |
| Sprint 4 | Attendance tracking and trainer assignments |
| Sprint 5 | Admin operations, validation, and error handling |
| Sprint 6 | API testing, documentation, deployment, and review |

Each sprint includes planning, implementation, testing, review, and retrospective activities.


#   Author

Pardha Gopi Krishna Yeedi

*Python Full Stack Developer*

#   License

This project is intended for learning and demonstration purposes. Add an appropriate open-source license, such as MIT, if you intend to distribute the project under those terms.

---

Gym Management System — Simplifying Gym Operations Through Technology.
