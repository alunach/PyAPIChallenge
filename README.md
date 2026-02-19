# 1 User Management API

### FastAPI + Docker + Google Cloud Run (Enterprise Deployment)

------------------------------------------------------------------------

## 2 Overview

This project implements a production-ready RESTful API for user
management using **FastAPI**, deployed in **Google Cloud Platform
(GCP)** using:

-   Cloud Build (CI)
-   Artifact Registry (Container storage)
-   Cloud Run (Serverless runtime)
-   IAM (Security & permissions)
-   Docker (Containerization)

The service follows clean architecture principles and is designed to be
scalable, maintainable, and cloud-native.

------------------------------------------------------------------------

## 3 Architecture Overview

Client → Cloud Run → FastAPI → SQLAlchemy → Database

CI/CD Flow:

Cloud Build → Artifact Registry → Cloud Run

------------------------------------------------------------------------

## 4 Tech Stack

-   Python 3.11
-   FastAPI
-   SQLAlchemy 2.x
-   Pydantic v2
-   Docker
-   Google Cloud Build
-   Google Artifact Registry
-   Google Cloud Run

------------------------------------------------------------------------

## 5 Project Structure

app/ 
├── api/ 
├── core/ 
├── db/ 
├── schemas/ 
├── services/ 
└── main.py
tests/ 
Dockerfile 
cloudbuild.yaml 
requirements.txt 
README.md

------------------------------------------------------------------------

# 6 Google Cloud Deployment Guide

## 6.1. Environment Variables (Windows CMD)


set PROJECT_ID=project-a716xxxx-63xx-4fxx-bxx
set REGION=us-central1
set REPO=user-api-repo
set IMAGE=user-api

------------------------------------------------------------------------

## 6.2. Enable Required APIs

gcloud services enable artifactregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com logging.googleapis.com

------------------------------------------------------------------------

## 6.3. IAM Configuration

Grant minimal required permissions:

gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" --role="roles/logging.logWriter"

------------------------------------------------------------------------

## 6.4. Create Artifact Registry Repository

gcloud artifacts repositories create %REPO% --repository-format=docker --location=%REGION% --description="Docker repository for user-api"

------------------------------------------------------------------------

## 7 Build & Push Container

gcloud builds submit --tag %REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO%/%IMAGE%


------------------------------------------------------------------------

## 8 Deploy to Cloud Run

gcloud run deploy %IMAGE% --image %REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO%/%IMAGE% --region %REGION% --platform managed --allow-unauthenticated

  
------------------------------------------------------------------------

# 9 Live Service

https://user-api-497614916082.us-central1.run.app

------------------------------------------------------------------------

# 10 Testing the API

## Health Check

GET /healthz

Example: https://user-api-497614916082.us-central1.run.app/api/healthz

Response: { "status": "ok" }

------------------------------------------------------------------------

## 11 Swagger Documentation

/docs

Example: https://user-api-497614916082.us-central1.run.app/docs

------------------------------------------------------------------------

## 12 Create User Example

curl -X POST https://user-api-497614916082.us-central1.run.app/users -H
"Content-Type: application/json" -d
"{"username":"alex","email":"alex@test.com","role":"admin"}"

------------------------------------------------------------------------

# 13 Security Considerations

-   IAM principle of least privilege
-   Serverless infrastructure
-   Containerized deployment
-   Logging integrated with Cloud Logging
-   Health endpoint for monitoring

------------------------------------------------------------------------

# 14 Scalability

Cloud Run provides:

-   Auto-scaling
-   Scale-to-zero
-   Revision management
-   Traffic splitting
-   Concurrency control

------------------------------------------------------------------------

# 15 CI/CD Strategy

cloudbuild.yaml automates:

1.  Docker image build
2.  Test execution
3.  Push to Artifact Registry
4.  Deployment to Cloud Run

------------------------------------------------------------------------

# 16 Challenge Submission JSON

{ "name": "Your Name", "mail": "your@email.com", "github_url":
"https://github.com/youruser/PyAPIChallenge.git", "api_url":
"https://user-api-497614916082.us-central1.run.app" }

------------------------------------------------------------------------

# 17 Verificación local

Antes de desplegar, prueba local con Docker:

docker build -t user-api .
docker run --rm -p 8080:8080 user-api


Luego abre:

http://localhost:8080/healthz

http://localhost:8080/docs

