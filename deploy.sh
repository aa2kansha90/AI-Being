#!/bin/bash

# Vercel Deployment Script for AI-Being Assistant

echo "🚀 Deploying AI-Being Assistant to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Install with: npm i -g vercel"
    exit 1
fi

# Deploy to Vercel
echo "📦 Deploying to production..."
vercel --prod

# Get deployment URL
DEPLOYMENT_URL=$(vercel ls | grep "ai-being-assistant" | head -1 | awk '{print $2}')

echo "✅ Deployment complete!"
echo "🌐 Live URL: https://$DEPLOYMENT_URL"
echo "🏥 Health Check: https://$DEPLOYMENT_URL/health"
echo "🔗 API Endpoint: https://$DEPLOYMENT_URL/api/assistant"

# Test deployment
echo "🧪 Testing deployment..."

# Test health endpoint
echo "Testing health endpoint..."
curl -s "https://$DEPLOYMENT_URL/health" | jq .

# Test API endpoint
echo "Testing API endpoint..."
curl -X POST "https://$DEPLOYMENT_URL/api/assistant" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Hello, test deployment", "session_id": "deploy_test"}' | jq .

echo "🎉 Deployment and testing complete!"
echo "📋 Run demo scenarios from DEMO_SCENARIOS.md"