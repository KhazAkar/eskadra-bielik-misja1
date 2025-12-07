#!/bin/bash

# Source environment variables
source reload-env.sh

# Deploy Bielik service to Cloud Run
gcloud run deploy "$BIELIK_SERVICE_NAME" \
    --source llamacpp-bielik/ \
    --region "$GOOGLE_CLOUD_LOCATION" \
    --concurrency 7 \
    --cpu 8 \
    --gpu 1 \
    --gpu-type nvidia-l4 \
    --max-instances 1 \
    --memory 16Gi \
    --allow-unauthenticated \
    --no-cpu-throttling \
    --no-gpu-zonal-redundancy \
    --timeout 3600 \
    --labels dev-tutorial=codelab-dos-"$BIELIK_EVENT_ID"
