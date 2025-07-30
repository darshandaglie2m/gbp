# GBP Manager

A dockerized web application for managing Google Business Profile audits and analytics. Users can create multiple projects, configure company details, connect to Google services, and receive AI-powered recommendations.

## Components

- **Backend**: Python FastAPI application with PostgreSQL database.
- **Frontend**: React + Material-UI interface.
- **OpenAI**: Generates recommendations for improving Google Business Profiles.
- **Google APIs**: Pulls GBP details and reviews for audit.

## Development

```bash
# build services
docker-compose build
# run stack
docker-compose up
```

Set the following environment variables before running:

- `OPENAI_API_KEY` - your OpenAI API key
- `GOOGLE_SERVICE_ACCOUNT_FILE` - path to a Google service account JSON key with
  access to the Business Profile APIs

Run backend type checks:

```bash
python -m py_compile backend/app/*.py
```

Access the API at `http://localhost:8000` and the frontend at `http://localhost:3000`.
