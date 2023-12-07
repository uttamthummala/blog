
# Django Blog CMS

Django Blog CMS is a simple content management system (CMS) built using Django. It allows users to create, edit, and manage blog articles through a web interface.

## Features

- User authentication (register, login, logout)
- Article management (create, edit, delete)
- Database storage for articles and user information
- WYSIWYG editor for article content
- Article listing with pagination, search, and filter options
- User roles (regular users and administrators)
- File uploads for article attachments
- Security measures against common web vulnerabilities
- Unit tests to ensure functionality and security
- Responsive and styled web interface

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/django-blog-cms.git
   cd django-blog-cms
2. Create a Virtual Environment:
   ```bash
   python -m venv venv
3. Activate the Virtual Environment:
   ```bash
   source venv/bin/activate
4. Install Dependencies:
   ```bash
   pip install -r requirements.txt
5. Apply Migrations:
   ```bash
   python manage.py migrate
6. Run the Development Server:
   ```bash
   python manage.py runserver
7. Run the Tests:
   ```bash
   python manage.py test
