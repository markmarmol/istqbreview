# Google Cloud Deployment Guide

## Prerequisites

1. **Google Cloud Project** - Create one at [console.cloud.google.com](https://console.cloud.google.com)
2. **gcloud CLI** - Install from [cloud.google.com/sdk](https://cloud.google.com/sdk/docs/install)
3. **Docker** - Install from [docker.com](https://www.docker.com/products/docker-desktop)
4. **API Keys & Credentials** - Set up Google Gemini and OpenAI API keys

## Setup Steps

### 1. Initialize gcloud and authenticate

```bash
gcloud init
gcloud auth login
```

### 2. Set your project ID

```bash
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID
```

### 3. Enable required APIs

```bash
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  containerregistry.googleapis.com
```

### 4. Set up environment variables using Secret Manager

```bash
# Create secrets for API keys
echo -n "your-google-api-key" | gcloud secrets create GOOGLE_API_KEY --data-file=-
echo -n "your-openai-api-key" | gcloud secrets create OPENAI_API_KEY --data-file=-

# Grant Cloud Run service access to secrets
gcloud secrets add-iam-policy-binding GOOGLE_API_KEY \
  --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor

gcloud secrets add-iam-policy-binding OPENAI_API_KEY \
  --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor
```

### 5. Build and deploy to Cloud Run

```bash
# Deploy using Cloud Build (recommended)
gcloud run deploy istqb-review \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --set-env-vars "GOOGLE_API_KEY=projects/PROJECT_ID/secrets/GOOGLE_API_KEY/latest,OPENAI_API_KEY=projects/PROJECT_ID/secrets/OPENAI_API_KEY/latest"
```

Or use Docker locally first:

```bash
# Build Docker image
docker build -t istqb-review:latest .

# Test locally
docker run -p 8080:8080 \
  -e GOOGLE_API_KEY="your-key" \
  -e OPENAI_API_KEY="your-key" \
  istqb-review:latest

# Push to Google Container Registry
docker tag istqb-review:latest gcr.io/$PROJECT_ID/istqb-review:latest
docker push gcr.io/$PROJECT_ID/istqb-review:latest

# Deploy from registry
gcloud run deploy istqb-review \
  --image gcr.io/$PROJECT_ID/istqb-review:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi
```

## Deployment Options

### Option A: Cloud Run (Recommended - Serverless)
- **Pros**: Automatic scaling, serverless, pay-per-use, easy updates
- **Cons**: Cold starts, 15-minute request limit
- **Best for**: Web applications, APIs

### Option B: App Engine (Standard/Flex)
- **Pros**: Built-in monitoring, easy deployment, managed infrastructure
- **Cons**: Less flexible, always charges minimum
- **Best for**: Long-running applications

### Option C: Compute Engine (VMs)
- **Pros**: Full control, persistent storage
- **Cons**: Manual scaling, always running
- **Best for**: Complex applications with special needs

## Monitoring & Logs

```bash
# View logs
gcloud run logs read istqb-review --limit=100

# Monitor in real-time
gcloud alpha run services describe istqb-review --region=us-central1

# View metrics in Console
# https://console.cloud.google.com/run/detail/us-central1/istqb-review
```

## Update & Rollback

```bash
# Deploy new version
gcloud run deploy istqb-review --source . --region us-central1

# Rollback to previous version
gcloud run services update-traffic istqb-review --to-revisions REVISION_NAME=100
```

## Cost Optimization

1. **Set min instances to 0** for auto-scaling
2. **Use Cloud Run over App Engine** for better pricing
3. **Set memory to minimum needed** (512MB-2GB)
4. **Use regional deployment** for better performance

## Troubleshooting

### Build fails
- Check `gcloud builds log --limit=50`
- Ensure all files are in `.gcloudignore`

### Runtime errors
- View logs: `gcloud run logs read istqb-review`
- Check environment variables are set

### Slow startup
- Pre-warm the service with a scheduled Cloud Scheduler job
- Increase min instances if needed

## Clean up

```bash
# Delete the Cloud Run service
gcloud run services delete istqb-review --region us-central1

# Delete images from registry
gcloud container images delete gcr.io/$PROJECT_ID/istqb-review --quiet

# Delete secrets
gcloud secrets delete GOOGLE_API_KEY OPENAI_API_KEY
```
