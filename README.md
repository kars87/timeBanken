# TimePortal

TimePortal is a time tracking and project management application built with Django. It allows users to track time spent on projects, manage materials, and generate reports.

## Features

- **Project Management**: Create, edit, and delete projects
- **Time Tracking**: Log time entries for projects with descriptions
- **Material Tracking**: Track materials used in projects with costs
- **Customer Management**: Associate projects with customers
- **Reporting**: View hours by day, week, month, or custom date ranges
- **Project Archive**: Separate view for completed projects
- **User Authentication**: Secure login and user-specific views

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/timeportal.git
   cd timeportal
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Usage

### Projects

- **View Projects**: Navigate to the Projects page to see all active projects
- **Create Project**: Click "Create New Project" to add a new project
- **Project Details**: Click on a project to view details, time entries, and materials
- **Edit/Delete**: Use the buttons on the project detail page to edit or delete a project
- **Mark as Finished**: Use the "Mark as Finished" button to move a project to the archive

### Time Entries

- **Add Time**: From a project detail page, click "Add Time Entry"
- **Edit/Delete Time**: Use the buttons next to each time entry
- **View Hours Overview**: Click "My Hours" in the navigation to see filtered time reports

### Materials

- **Add Materials**: From a project detail page, click "Add Material"
- **Edit/Delete Materials**: Use the buttons next to each material

### Admin Interface

Access the admin interface at http://127.0.0.1:8000/admin/ to manage all aspects of the application.

## Project Structure

- `timetracker/` - Main Django project directory
- `projects/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions
  - `urls.py` - URL routing
  - `forms.py` - Form definitions
  - `admin.py` - Admin interface configuration
  - `templates/` - HTML templates

## License

[Your License Here]

## Contact

[Your Contact Information]