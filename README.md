# GBP Manager

A dockerized web application for managing Google Business Profile audits and analytics. Users can create multiple projects, configure company details, connect to Google services, and receive AI-powered recommendations.

## Components

- **Backend**: Python FastAPI application with PostgreSQL database.
- **Frontend**: React + Material-UI interface.
- **OpenAI**: Generates recommendations for improving Google Business Profiles.

## Development

```bash
# build services
docker-compose build
# run stack
docker-compose up
```

Access the API at `http://localhost:8000` and the frontend at `http://localhost:3000`.
