# SeuEmprego

A simple job board web application built with Flask, allowing users to post and manage job listings.

## Features

- User authentication (register, login, logout)
- Password reset functionality via email
- Job listing creation and management
- Admin panel for user and listing management
- Personal dashboard for managing your job listings

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: MySQL (with SQLAlchemy ORM)
- **Authentication**: Werkzeug Security
- **Email**: Flask-Mail
- **Frontend**: Bootstrap 5
- **Environment Variables**: python-dotenv

## Installation

1. Clone the repository
   ```bash
   git clone git@github.com:pablodeas/seuemprego.git
   cd seuemprego
   ```

2. Create a virtual environment and activate it
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DB_USERNAME=your_db_username
   DB_PASSWORD=your_db_password
   DB_HOSTNAME=your_db_hostname
   DB_DATABASE=your_db_name
   MAIL_USERNAME=your_email@example.com
   MAIL_PASSWORD=your_email_password
   ```

## Database Setup

The application uses SQLAlchemy with a MySQL database. Make sure to create the database before running the application.

The models include:
- `Usuario` (User): Stores user information and authentication data
- `Vaga` (Job): Stores job listing information

## Running the Application

```bash
python flask_app.py
```

The application will be available at `http://localhost:5000`

## Routes

- `/`: Home page displaying all job listings
- `/login`: User login page
- `/logout`: User logout
- `/register`: User registration page
- `/add_vaga`: Add a new job listing (requires login)
- `/privado`: Personal dashboard showing your job listings
- `/delete_vaga/<id>`: Delete a job listing (requires ownership)
- `/reset_password`: Request password reset via email
- `/reset_password/<token>`: Reset password with token
- `/admin`: Admin dashboard (requires admin privileges)

## Security Features

- Password hashing with Werkzeug
- Secure session management
- Token-based password reset
- Permission-based access control
- User ownership verification for content management

## Deployment Notes

This application is configured for deployment, with environment variable support. Before deploying:

1. Set `app.config["DEBUG"] = False` (already configured)
2. Configure a proper secret key for production
3. Set up a production-ready database connection
4. Configure email settings for a production environment

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.