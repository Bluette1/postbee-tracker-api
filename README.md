# PostBee Tracker API

## Overview

The PostBee Tracker API is a microservices-based backend designed to support the PostBee application. This API manages job applications and enhances user interactions with job posts. Key functionalities include handling pinned job posts, saved job posts, user journal notes, analytics, and powerful searching and filtering capabilities.

[Postbee Tracker API Url](https://postbee-tracker-api-438f610a3ed6.herokuapp.com)

## Features

### Job Post Management

- **Pinned Job Posts**: Allows employers to pin job listings for increased visibility.
- **Saved Job Posts**: Users can save job posts for easy access later.

### User Interaction

- **Follow-Ups**: Users can set reminders for follow-ups on job applications.
- **Viewed Job Posts**: Track job postings the user has interacted with.

### Journal Notes

- **User Journal**: Users can maintain personal notes about job applications and interviews.

### Analytics

- **Weekly Reports**: Provides employers with summaries of job posting performances and user engagement statistics.

### Searching and Filtering

- **Job Search**: Users can search and filter job postings by keywords and various criteria.

## User Stories

This API is built around the following user stories:

- **As an employer**, I want to pin job posts, so they are more visible to potential applicants.
- **As a job seeker**, I want to save job posts for later review.
- **As a user**, I want to receive follow-up reminders for my job applications.
- **As a job seeker**, I want to view my job search history through the job posts I've interacted with.
- **As a user**, I want to maintain a journal of notes about my job applications.
- **As an employer**, I want to receive weekly reports on job posting performance.
- **As a job seeker**, I want to view statistics on the jobs I’ve applied for.
- **As a job seeker**, I want to search for jobs using keywords and filter results to find relevant opportunities.
- **As an employer**, I want to filter job applications based on specific criteria.

## API Endpoints

### Job Post Management

- `POST /job_posts/pin` - Pin a job post to the top of listings.
- `GET /job_posts/saved` - Retrieve saved job posts for the user.

### User Interaction

- `POST /applications/follow_up` - Create a follow-up reminder for a job application.
- `GET /job_posts/viewed` - Retrieve viewed job posts.

### Journal Notes

- `POST /journal/notes` - Add a new journal note.
- `GET /journal/notes` - Retrieve user's journal notes.

### Analytics

- `GET /analytics/weekly_reports` - Retrieve weekly job reports.

### Searching and Filtering

- `GET /job_posts/search` - Search job posts with keywords and filters.

## Authentication

All API endpoints require user authentication. Ensure to include a valid token in the request headers for access to protected resources.

## Running the Application

To run the application, you need to start both the Flask web server and the Celery worker. Follow the steps below:

### 1. Start the Flask App

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/postbee-tracker-api.git
   cd postbee-tracker-api
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask application:
   ```bash
   flask run
   ```

### 2. Start the Celery Worker

In a separate terminal window, navigate to your project directory again and run the following command to start the Celery worker:

```bash
celery -A app.celery worker --loglevel=info
```

Replace `app` with the actual module name where your `celery` instance is defined if it's different. The `--loglevel=info` option will provide you with informative logging output in the terminal.

### Note

- Ensure that you have all necessary dependencies installed and your database is properly configured before running the application.
- If you are using Docker, you may have a separate service defined in your `docker-compose.yml` file for the Celery worker. Make sure to start that service as well.


### 3. Running the Consumer

To start the consumer that processes messages from RabbitMQ and sends follow-up notifications, follow these steps:

### Prerequisites

- Ensure that RabbitMQ is running.
   ```
   sudo systemctl start rabbitmq-server
   ```
- Make sure your virtual environment is activated, if you are using one.

### Starting the Consumer

1. Navigate to the project root directory:

   ```bash
   cd ~/workspace/postbee-tracker-api
   ```

2. Run the consumer using the following command:

   ```bash
   python -m webapp.consumer
   ```

This command will start the consumer, which will listen for messages on the `followup_notifications` queue. To stop the consumer, you can press `CTRL+C` in the terminal where it is running.

````


## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and continuous deployment. The pipeline includes:

### Automated Checks

- Code formatting (Black)
- Import sorting (isort)
- Linting (flake8)
- Unit tests (pytest)
- Code coverage reporting

### Workflow Triggers

The CI pipeline runs on:

- Push to main and develop branches
- Pull requests to main and develop branches

### Local Development

To run the same checks locally before committing:

```bash
# Install development dependencies
pip install black flake8 pytest pytest-cov isort

# Format code
black .
isort .

# Run linting
flake8

# Run tests with coverage
pytest --cov=.
````

## Contributing

Contributions are welcome! Please fork the repository and create a new feature branch. Submit a pull request with your changes.

### [User Stories](https://www.notion.so/PostBee-Tracker-API-User-Stories-153e6a4d98f280a5a34aebfe656b1306?pvs=12)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Thank you to all contributors and users for their feedback and support in developing the PostBee Tracker API.
