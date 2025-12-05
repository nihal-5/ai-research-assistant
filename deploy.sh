#!/bin/bash

# Script to create GitHub repo and push code
# Run this to complete the deployment

echo "Creating GitHub repository..."
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: ai-research-assistant"
echo "3. Description: Multi-agent AI system for automated research and report generation using CrewAI"
echo "4. Select: Public"
echo "5. DO NOT check 'Add a README file'"
echo "6. Click 'Create repository'"
echo ""
read -p "Press ENTER after you've created the repository..."

echo ""
echo "Adding remote and pushing code..."
git remote add origin https://github.com/nihal-5/ai-research-assistant.git 2>/dev/null || git remote set-url origin https://github.com/nihal-5/ai-research-assistant.git
git push -u origin main

echo ""
echo "✅ Done! Your project is now live at:"
echo "https://github.com/nihal-5/ai-research-assistant"
