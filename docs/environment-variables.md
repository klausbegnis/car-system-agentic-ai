# Environment Variables

This guide explains how to configure environment variables for the Car System Agentic AI project.

## Overview

The project uses environment variables to manage sensitive configuration like API keys and other settings. These are loaded from a `.env` file in the project root.

## Setup

### 1. Create Environment File

Create a `.env` file in the project root directory:

```bash
# Copy the example file (if available)
cp .env.example .env

# Or create manually
touch .env
```

### 2. Required Variables

Add the following variables to your `.env` file:

```bash
# Google AI API Key (Required)
GOOGLE_API_KEY=your_google_api_key_here
```

## Variable Descriptions

### Required Variables

#### `GOOGLE_API_KEY`
- **Purpose**: Authentication for Google Gemini AI models
- **Required**: Yes
- **Format**: String (API key from Google AI Studio)
- **Example**: `GOOGLE_API_KEY=AIzaSyC9X8Y7Z6W5V4U3T2S1R0Q9P8O7N6M5L4K3`

**How to get your API key:**
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" 
4. Create a new API key or use an existing one
5. Copy the key to your `.env` file
