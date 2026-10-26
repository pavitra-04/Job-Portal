# Job Portal

A web-based job portal built using Django that connects job seekers with employers. Candidates can explore opportunities and track applications, while employers can publish jobs and manage applicants.

## Features

### Candidates
- Register and log in.
- Browse and search job listings.
- Filter jobs by location and job type.
- View detailed job descriptions.
- Apply for jobs and prevent duplicate applications.
- Track application status.

### Employers
- Register and log in.
- Create, edit, and delete job postings.
- View applicants for their jobs.
- Update application statuses to Pending, Shortlisted, or Rejected.

### General
- Role-based access control.
- Responsive styling with HTML and CSS.
- Automated tests for core functionality and permissions.

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Django Templates
- **Database:** SQLite
- **Testing:** Django TestCase

## Getting Started

### Prerequisites
- Python 3.14 or a compatible Python version
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/pavitra-04/Job-Portal.git
   cd Job-Portal
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   python3 -m pip install Django
   ```

4. Apply database migrations:

   ```bash
   python3 manage.py migrate
   ```

5. Start the development server:

   ```bash
   python3 manage.py runserver
   ```

6. Open `http://127.0.0.1:8000/` in your browser.

## Running Tests

Run the automated tests with:

```bash
python3 manage.py test
```

## Future Improvements

- Resume uploads and candidate profiles.
- Email notifications for application updates.
- Pagination and advanced job filters.
- Production deployment.

## Author

**Pavitra Singh**

Built as a Django web development project.
