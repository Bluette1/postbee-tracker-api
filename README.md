
# PostBee Tracker API

## Overview

The PostBee Tracker API is a microservices-based backend designed to support the PostBee application. This API manages job applications and enhances user interactions with job posts. Key functionalities include handling pinned job posts, saved job posts, user journal notes, analytics, and powerful searching and filtering capabilities.

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

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/postbee-tracker-api.git
   cd postbee-tracker-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask application:
   ```bash
   flask run
   ```

## Contributing

Contributions are welcome! Please fork the repository and create a new feature branch. Submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Thank you to all contributors and users for their feedback and support in developing the PostBee Tracker API.
