# 1 User Management API

Production-oriented FastAPI service implementing a user CRUD API with:
- Clean architecture (router → service → repository)
- SQLAlchemy 2.0 + Alembic migrations
- Strong validation with Pydantic (EmailStr, enums, constraints)
- Structured logging + request id
- Health endpoints
- Comprehensive pytest suite + coverage
- Cloud Build pipeline: test → build → deploy to Cloud Run

------------------------------------------------------------------------

## 1.1. API base
- **Base path:** `/api/v1`
- **Docs:** `/api/v1/docs`
- **OpenAPI:** `/api/v1/openapi.json`

------------------------------------------------------------------------

## 1.2. Endpoints
### Health
- `GET /api/v1/health/live`
- `GET /api/v1/health/ready`

### 1.2.1. Users
- `POST   /api/v1/users`
- `GET    /api/v1/users?active=true&limit=50&offset=0`
- `GET    /api/v1/users/{user_id}`
- `PUT    /api/v1/users/{user_id}`
- `DELETE /api/v1/users/{user_id}` (soft delete: sets `active=false`)

------------------------------------------------------------------------

## 1.3. Running locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt

# Use SQLite by default
export DATABASE_URL="sqlite:///./app.db" 
# Windows: set DATABASE_URL=sqlite:///./app.db
alembic upgrade head
uvicorn app.main:app --reload --port 8080
```

Open:
- http://localhost:8080/api/v1/docs

------------------------------------------------------------------------

## 1.4. Example API calls
Create:
```bash
curl -i -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username":"alex01","email":"alex01@example.com","first_name":"Alex","last_name":"Test","role":"user"}'
```

List:
```bash
curl -i "http://localhost:8080/api/v1/users?limit=50&offset=0"
```

Get:
```bash
curl -i http://localhost:8080/api/v1/users/<USER_ID>
```

Update:
```bash
curl -i -X PUT http://localhost:8080/api/v1/users/<USER_ID> \
  -H "Content-Type: application/json" \
  -d '{"role":"admin","active":true}'
```

Soft delete:
```bash
curl -i -X DELETE http://localhost:8080/api/v1/users/<USER_ID>
```

------------------------------------------------------------------------

## 1.5. Testing
```bash
pytest -q --cov=app --cov-report=term-missing
```

------------------------------------------------------------------------

## 1.6. Configuration
Environment variables (see `.env.example`):
- `DATABASE_URL` (default: `sqlite:///./app.db`)
- `LOG_LEVEL` (default: `INFO`)
- `APP_NAME` (default: `user-api`)

------------------------------------------------------------------------

## 1.7. Deploy (Cloud Build + Cloud Run)
This repository includes `cloudbuild.yaml` that:
1) runs unit tests
2) builds Docker image and pushes to Artifact Registry
3) deploys to Cloud Run

Update variables in `cloudbuild.yaml`:
- `_REGION`
- `_SERVICE_NAME`
- `_REPO`
- `_IMAGE`

Then run:
```bash
gcloud builds submit --config cloudbuild.yaml
```

------------------------------------------------------------------------

### 1.7.1. Environment Variables (Windows CMD)

```bash
set PROJECT_ID=project-a71xxxxx-63xx-4fxx-bxx
set PROJECT_NUMBER=497xxxxxxxx
set REGION=us-central1
set REPO=user-api-repo
set IMAGE=user-api
```

------------------------------------------------------------------------

### 1.7.2. Enable Required APIs

```bash
gcloud services enable artifactregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com logging.googleapis.com
```

------------------------------------------------------------------------

### 1.7.3. IAM Configuration

Grant minimal required permissions:

```bash
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%PROJECT_NUMBER%-compute@developer.gserviceaccount.com" --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%PROJECT_NUMBER%@cloudbuild.gserviceaccount.com" --role="roles/run.admin"

gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%PROJECT_NUMBER%@cloudbuild.gserviceaccount.com" --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%PROJECT_NUMBER%@cloudbuild.gserviceaccount.com" --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%PROJECT_NUMBER%-compute@developer.gserviceaccount.com" --role="roles/run.admin"

gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%PROJECT_NUMBER%-compute@developer.gserviceaccount.com" --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%PROJECT_NUMBER%-compute@developer.gserviceaccount.com" --role="roles/artifactregistry.writer"
```


------------------------------------------------------------------------

### 1.7.4. Create Artifact Registry Repository

```bash
gcloud artifacts repositories create %REPO% --repository-format=docker --location=%REGION% --description="Docker repository for user-api"
```

------------------------------------------------------------------------

### 1.7.5. Build & Push Container

```bash
gcloud builds submit --tag %REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO%/%IMAGE%
gcloud run deploy %IMAGE% --image %REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO%/%IMAGE% --region %REGION% --platform managed --allow-unauthenticated
```

or:

```bash
gcloud builds submit --config cloudbuild.yaml
```
  
------------------------------------------------------------------------

### 1.7.7. Live Service

https://user-api-497614916082.us-central1.run.app

------------------------------------------------------------------------

### 1.7.8. Testing the API

### Health Check

GET /healthz

Example: https://user-api-497xxxxxxxx.us-central1.run.app/api/v1/healthz

Response: { "status": "ok" }


### Swagger Documentation

/docs

Example: https://user-api-497xxxxxxxx.us-central1.run.app/api/v1/docs

### Create User Example

curl -X POST https://user-api-497xxxxxxxx.us-central1.run.app/users -H
"Content-Type: application/json" -d
"{"username":"alex","email":"alex@test.com","role":"admin"}"

### Import Postman Collection

Import from:

postman/users.postman_collection.json

```bash
https://github.com/alunach/PyAPIChallenge/tree/main/postman
```



------------------------------------------------------------------------

### 1.7.9. Security Considerations

-   IAM principle of least privilege
-   Serverless infrastructure
-   Containerized deployment
-   Logging integrated with Cloud Logging
-   Health endpoint for monitoring

------------------------------------------------------------------------

### 1.7.10. Scalability

Cloud Run provides:

-   Auto-scaling
-   Scale-to-zero
-   Revision management
-   Traffic splitting
-   Concurrency control

------------------------------------------------------------------------

### 1.7.11. CI/CD Strategy

cloudbuild.yaml automates:

1.  Docker image build
2.  Test execution
3.  Push to Artifact Registry
4.  Deployment to Cloud Run

------------------------------------------------------------------------

### 1.7.12. Local Verifitacion with Docker

Before deploying, test locally with Docker:

docker build -t user-api .
docker run --rm -p 8080:8080 user-api


Then open URLs:

http://localhost:8080/api/v1/healthz

http://localhost:8080/api/v1/docs

...
